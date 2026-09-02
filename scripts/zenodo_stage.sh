#!/usr/bin/env bash
# Stage the TR2 v1.0 files and metadata onto the reserved Zenodo draft.
#
#   printf %s "$(pbpaste)" > ~/.zenodo-token && chmod 600 ~/.zenodo-token
#   ./scripts/zenodo_stage.sh <report-slug> --dry-run   # GETs only, mutates nothing
#   ./scripts/zenodo_stage.sh <report-slug>
#
# Report-specific values live in reports/<slug>/release.conf.
#
# NEVER PUBLISHES. Publishing needs the deposit:actions scope and the publish
# endpoint; this script calls neither. Scope the token to deposit:write and the
# irreversible step becomes impossible rather than merely unexercised.
#
# A published Zenodo record can gain a new version but can never lose or replace
# a file. Publish by hand, in the UI, after reviewing the staged draft.
#
# Ordering is additive-first on purpose: upload and verify the new files BEFORE
# deleting the old one, so an interrupted run leaves a draft with too many files
# rather than none.
set -euo pipefail

API=https://zenodo.org/api
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SLUG="${1:?usage: zenodo_stage.sh <report-slug> [--dry-run]}"
CONF="$ROOT/reports/$SLUG/release.conf"
[ -r "$CONF" ] || { echo "  FAIL: no release.conf at $CONF" >&2; exit 1; }
# shellcheck disable=SC1090
source "$CONF"
DEP_ID="$ZENODO_DEP_ID"
PDF="$ROOT/reports/$SLUG/report/$PDF_NAME"
ZIP="$ROOT/dist/$ZIP_BASE.zip"
URL="$REPORT_URL"
DRY=0; [ "${2:-}" = "--dry-run" ] && DRY=1

fail(){ echo "  FAIL: $*" >&2; exit 1; }
ok(){   echo "  ok   $*"; }
note(){ echo "  --   $*"; }

TOKEN_FILE="${ZENODO_TOKEN_FILE:-$HOME/.zenodo-token}"
if [ -z "${ZENODO_TOKEN:-}" ] && [ -r "$TOKEN_FILE" ]; then
  ZENODO_TOKEN="$(tr -d '\r\n' < "$TOKEN_FILE")"
  perms=$(stat -f '%A' "$TOKEN_FILE" 2>/dev/null || stat -c '%a' "$TOKEN_FILE" 2>/dev/null || echo unknown)
  [ "$perms" = "600" ] || fail "$TOKEN_FILE is mode $perms. Refusing to read a token from a\n        world- or group-readable file. Run: chmod 600 $TOKEN_FILE"
fi
: "${ZENODO_TOKEN:?no token. Write it to ~/.zenodo-token (chmod 600) or export ZENODO_TOKEN. Never paste it into a chat or a command line.}"

# Every call checks its HTTP status. curl exits 0 on a 4xx/5xx, so without this
# a failed DELETE or upload looks exactly like a successful one.
BODY=$(mktemp); trap 'rm -f "$BODY"' EXIT
api(){  # api METHOD URL [curl args...] -> body on stdout; aborts on non-2xx
  local method="$1" url="$2"; shift 2
  local code
  code=$(curl -sS -o "$BODY" -w '%{http_code}' --max-time 300 \
         -X "$method" -H "Authorization: Bearer $ZENODO_TOKEN" "$@" "$url") \
    || fail "$method $url — curl transport error"
  case "$code" in
    2*) cat "$BODY" ;;
    *)  echo "  HTTP $code from $method $url" >&2
        head -c 400 "$BODY" >&2; echo >&2
        fail "$method returned HTTP $code" ;;
  esac
}
jq_py(){ python3 -c "import json,sys; d=json.load(sys.stdin); $1"; }

md5_of(){ md5 -q "$1" 2>/dev/null || md5sum "$1" | awk '{print $1}'; }

echo "== 0. local artifacts =="
[ -f "$PDF" ] || fail "no v1.0 PDF — run assemble_release.sh first"
[ -f "$ZIP" ] || fail "no public ZIP — run assemble_release.sh first"
command -v pdftotext >/dev/null || fail "pdftotext not found (brew install poppler)"
pdftotext "$PDF" "$BODY.txt"
for s in "${PDF_FORBID[@]}"; do
  grep -qF "$s" "$BODY.txt" && fail "that PDF contains \"$s\" -- it is a draft"
done
for r in "${PDF_REQUIRE_REGEX[@]}"; do
  grep -qE "$r" "$BODY.txt" || fail "PDF is missing required content: /$r/"
done
rm -f "$BODY.txt"
ok "PDF is the v1.0 build"
PDF_MD5=$(md5_of "$PDF"); ZIP_MD5=$(md5_of "$ZIP")
ok "local md5  PDF $PDF_MD5"
ok "local md5  ZIP $ZIP_MD5"

echo "== 1. read the draft =="
DEP=$(api GET "$API/deposit/depositions/$DEP_ID")
printf '%s' "$DEP" | jq_py "
assert not d.get('submitted'), 'ALREADY PUBLISHED — refusing to touch it'
print('  ok   state=%s submitted=%s' % (d.get('state'), d.get('submitted')))
print('  ok   bucket present' if d.get('links',{}).get('bucket') else '  FAIL no bucket link')
for f in d.get('files',[]): print('  --   existing: %s md5:%s' % (f['filename'], f['checksum']))
"
# Identity gate. Everything after this point writes. If API or DEP_ID were
# ever wrong, or a bucket link pointed elsewhere, uploads would land on someone
# else's record and every later check would pass against the wrong target.
printf '%s' "$DEP" | DEP_ID="$DEP_ID" DOI="$DOI" python3 -c "
import json,os,sys
d=json.load(sys.stdin)
want_id=os.environ['DEP_ID']; want_doi=os.environ['DOI']
got_id=str(d.get('id') or d.get('record_id') or '')
if got_id != want_id: sys.exit('  FAIL: deposition id is %r, expected %r' % (got_id, want_id))
m=d.get('metadata',{})
doi=(m.get('prereserve_doi') or {}).get('doi') or m.get('doi') or d.get('doi') or ''
if doi != want_doi: sys.exit('  FAIL: reserved DOI is %r, expected %r' % (doi, want_doi))
b=d.get('links',{}).get('bucket','')
# Live Zenodo buckets are https://zenodo.org/api/files/<uuid> — they contain
# neither the deposition id nor the word 'bucket'. Validate scheme and host, not
# a substring that only ever matched the mock.
from urllib.parse import urlparse
u=urlparse(b)
allowed={'zenodo.org','sandbox.zenodo.org'}
override=os.environ.get('ZENODO_ALLOW_HOST','')
if override: allowed.add(override)
if u.scheme not in ('https','http') or not u.netloc:
    sys.exit('  FAIL: bucket link is not a URL: %r' % b)
host=u.netloc.split(':')[0]
if host not in allowed:
    sys.exit('  FAIL: bucket host %r is not one of %s' % (host, sorted(allowed)))
if u.scheme != 'https' and host not in ('127.0.0.1','localhost'):
    sys.exit('  FAIL: refusing a non-https bucket on %r' % host)
print('  ok   identity: deposition %s, DOI %s' % (got_id, doi))
" || exit 1
# Preflight: refuse an unexpected file BEFORE uploading anything, so a stranger
# file means zero writes rather than two uploads and then an abort.
DESIRED="$(basename "$PDF"):$PDF_MD5 $(basename "$ZIP"):$ZIP_MD5"
printf '%s' "$DEP" | DESIRED="$DESIRED" python3 -c "
import json,os,sys
d=json.load(sys.stdin)
want=set(dict(x.split(':',1) for x in os.environ['DESIRED'].split()))
extra=[f['filename'] for f in d.get('files',[]) if f['filename'] not in want]
if extra:
    sys.exit('  FAIL: unexpected files already on the draft: %s\\n'
             '        nothing has been uploaded. Remove them in the Zenodo UI if\\n'
             '        they do not belong, then re-run.' % extra)
print('  ok   no unexpected files on the draft')
" || exit 1
BUCKET=$(printf '%s' "$DEP" | jq_py "print(d['links']['bucket'])")

if [ "$DRY" = 1 ]; then
  echo; echo "DRY RUN — read-only. Nothing uploaded, deleted, or modified."; exit 0
fi

echo "== 2. upload the new files FIRST (additive) =="
for f in "$PDF" "$ZIP"; do
  n=$(basename "$f"); want=$(md5_of "$f")
  got=$(api PUT "$BUCKET/$n" --upload-file "$f" | jq_py "print(d.get('checksum','').replace('md5:',''))")
  [ "$got" = "$want" ] || fail "$n uploaded but checksum differs (local $want, remote $got)"
  ok "uploaded and verified $n  md5 $got"
done

echo "== 3. re-read, and prove the new bytes are actually on the record =="
# Identity, not names. The PDF is uploaded under the SAME bucket key as the file
# already there, so a name check cannot tell the new bytes from the old ones —
# and deleting by an id recorded before the upload can delete the replacement
# itself, if Zenodo keeps the id across a same-key overwrite. Everything below
# keys off checksums, which is true regardless of how ids behave.
DEP2=$(api GET "$API/deposit/depositions/$DEP_ID")
printf '%s' "$DEP2" | DESIRED="$DESIRED" python3 -c "
import json,os,sys
d=json.load(sys.stdin)
if d.get('submitted'): sys.exit('  FAIL: published mid-run — stopping before deleting anything')
want=dict(x.split(':',1) for x in os.environ['DESIRED'].split())
have={f['filename']: f['checksum'].replace('md5:','') for f in d.get('files',[])}
bad=[n for n,c in want.items() if have.get(n)!=c]
if bad: sys.exit('  FAIL: not on the record with the expected checksum: %s' % bad)
print('  ok   still unsubmitted; both files present with the exact local checksums')
" || exit 1

echo "== 4. refuse anything unexpected — this script never deletes =="
# The same-key PUT already replaced the old PDF, so there is nothing to remove.
# Deletion was the only destructive operation here; removing it removes the
# entire class of risk, including the one that made 23187b7 unsafe. If a file
# we did not put there is on the record, stop and let a person decide.
printf '%s' "$DEP2" | DESIRED="$DESIRED" python3 -c "
import json,os,sys
d=json.load(sys.stdin)
want=set(dict(x.split(':',1) for x in os.environ['DESIRED'].split()))
extra=[f['filename'] for f in d.get('files',[]) if f['filename'] not in want]
if extra:
    print('  FAIL: unexpected files on the draft: %s' % extra)
    print('        this script will not delete them. Remove them in the Zenodo UI')
    print('        if they do not belong, then re-run.')
    sys.exit(1)
print('  ok   record holds exactly the two intended files; nothing to delete')
" || exit 1

echo "== 5. metadata =="
REPORT_TITLE="$REPORT_TITLE" ZENODO_KEYWORDS="$ZENODO_KEYWORDS" ZENODO_SCOPE="$ZENODO_SCOPE" LICENSE_ID="$LICENSE_ID" \
  PUB_DATE="$PUB_DATE" VERSION="$VERSION" python3 - "$URL" > "$BODY.meta" <<'PYMETA'
import json,os,sys
url=sys.argv[1]
scope=os.environ["ZENODO_SCOPE"]
desc=("<p>We tested one frozen character post-training recipe across three model families. "
      "It reduced unsupported assertions, but no family preserved grounded-answer accuracy "
      "well enough to meet the pre-registered bar.</p>"
      f"<p><strong>Scope.</strong> {scope}</p>"
      "<p>This is an aggregate-only release. It does not contain item-level scored outputs, "
      "judge ledgers, benchmark prompt text, model weights, or the primary-test holdout, and "
      "does not support independent recomputation of the readout. See Appendix D of the report.</p>")
print(json.dumps({"metadata":{
 "upload_type":"publication","publication_type":"report",
 "title":os.environ["REPORT_TITLE"],
 "creators":[{"name":"Pu, George","affiliation":"SimpleDirect / Vinci Research"},
             {"name":"Naik, Ayush","affiliation":"SimpleDirect / Vinci Research"}],
 "description":desc,"publication_date":os.environ["PUB_DATE"],"version":os.environ["VERSION"],
 "language":"eng","access_right":"open","license":os.environ["LICENSE_ID"],
 "keywords":json.loads(os.environ["ZENODO_KEYWORDS"]),
 "related_identifiers":[{"identifier":url,"relation":"isIdenticalTo","scheme":"url"}],
 "notes":scope}},indent=2))
PYMETA
api PUT "$API/deposit/depositions/$DEP_ID" -H "Content-Type: application/json" -d @"$BODY.meta" >/dev/null
rm -f "$BODY.meta"; ok "metadata written"

echo "== 6. assert the end state (non-zero exit if anything is wrong) =="
api GET "$API/deposit/depositions/$DEP_ID" | DESIRED="$DESIRED" VERSION="$VERSION" LICENSE_ID="$LICENSE_ID" SCOPE_PROBE="$SCOPE_PROBE" python3 -c "
import json,os,sys
d=json.load(sys.stdin); m=d.get('metadata',{})
want=dict(x.split(':',1) for x in os.environ['DESIRED'].split())
have={f['filename']: f['checksum'].replace('md5:','') for f in d.get('files',[])}
errs=[]
if d.get('submitted'):          errs.append('record is submitted/published')
if m.get('version')!=os.environ['VERSION']: errs.append('version is %r, expected %r' % (m.get('version'), os.environ['VERSION']))
if m.get('license')!=os.environ['LICENSE_ID']: errs.append('licence is %r, expected %r' % (m.get('license'), os.environ['LICENSE_ID']))
if os.environ['SCOPE_PROBE'] not in (m.get('description') or ''):
    errs.append('configured scope line missing from description')
if set(have)!=set(want):        errs.append('files are %s, expected %s' % (sorted(have), sorted(want)))
for n,c in want.items():
    if have.get(n)!=c: errs.append('%s checksum %s, expected %s' % (n, have.get(n), c))
for n,c in sorted(have.items()): print('  file     :', n, c)
print('  version  :', m.get('version'), ' licence:', m.get('license'), ' submitted:', d.get('submitted'))
if errs:
    print('  >>> NOT STAGED CORRECTLY'); [print('      -',e) for e in errs]; sys.exit(1)
print('  >>> STAGED CORRECTLY')
" || fail "end-state assertion failed — inspect the draft before doing anything else"

echo
echo "Staged, NOT published. Review then publish by hand:"
echo "  https://zenodo.org/uploads/$DEP_ID"
