#!/usr/bin/env bash
# Stage the TR2 v1.0 files and metadata onto the reserved Zenodo draft.
#
#   printf %s "$(pbpaste)" > ~/.zenodo-token && chmod 600 ~/.zenodo-token
#   ./scripts/zenodo_stage.sh --dry-run     # GETs only, mutates nothing
#   ./scripts/zenodo_stage.sh
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

DEP_ID=22236690
API=https://zenodo.org/api
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF="$ROOT/reports/tr2/report/Vinci_Technical_Report_No_2.pdf"
ZIP="$ROOT/dist/Vinci-TR2-Character-Transfer-v1.0-public.zip"
URL="https://www.getsimpledirect.com/research/papers/character-transfer-across-three-model-families"
DRY=0; [ "${1:-}" = "--dry-run" ] && DRY=1

fail(){ echo "  FAIL: $*" >&2; exit 1; }
ok(){   echo "  ok   $*"; }
note(){ echo "  --   $*"; }

TOKEN_FILE="${ZENODO_TOKEN_FILE:-$HOME/.zenodo-token}"
if [ -z "${ZENODO_TOKEN:-}" ] && [ -r "$TOKEN_FILE" ]; then
  ZENODO_TOKEN="$(tr -d '\r\n' < "$TOKEN_FILE")"
  perms=$(stat -f '%A' "$TOKEN_FILE" 2>/dev/null || stat -c '%a' "$TOKEN_FILE" 2>/dev/null || echo unknown)
  [ "$perms" = "600" ] || echo "  WARN $TOKEN_FILE is mode $perms; chmod 600 it"
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
grep -q "Version 0.9"                   "$BODY.txt" && fail 'that PDF contains "Version 0.9" — it is the draft'
grep -q "Version 1.0 - 1 September 2026" "$BODY.txt" || fail 'title block is not the v1.0 line'
grep -q "Outstanding Evidence Work"      "$BODY.txt" || fail 'Appendix D is not the v1.0 text'
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
BUCKET=$(printf '%s' "$DEP" | jq_py "print(d['links']['bucket'])")
# Record exactly which file ids we intend to remove. Later we delete these ids
# and nothing else, so a file added by someone in the meantime is never touched.
OLD_IDS=$(printf '%s' "$DEP" | jq_py "print(' '.join(f['id'] for f in d.get('files',[])))")
note "will remove file ids: ${OLD_IDS:-<none>}"

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

echo "== 3. re-read before any destructive step =="
DEP2=$(api GET "$API/deposit/depositions/$DEP_ID")
printf '%s' "$DEP2" | jq_py "
assert not d.get('submitted'), 'record was PUBLISHED mid-run — stopping before deleting anything'
names={f['filename'] for f in d.get('files',[])}
for n in ['Vinci_Technical_Report_No_2.pdf','Vinci-TR2-Character-Transfer-v1.0-public.zip']:
    assert n in names, 'expected %s on the draft after upload, not found' % n
print('  ok   still unsubmitted, both new files present')
"

echo "== 4. remove only the file ids recorded in step 1 =="
for fid in $OLD_IDS; do
  still=$(printf '%s' "$DEP2" | jq_py "print('yes' if any(f['id']=='$fid' for f in d.get('files',[])) else 'no')")
  if [ "$still" != "yes" ]; then note "file id $fid already gone, skipping"; continue; fi
  api DELETE "$API/deposit/depositions/$DEP_ID/files/$fid" >/dev/null
  ok "deleted file id $fid"
done

echo "== 5. metadata =="
python3 - "$URL" > "$BODY.meta" <<'PY'
import json,sys
url=sys.argv[1]
scope=("Development-tier validation evidence only. Refusal adjustment is Judge-B-only. "
       "Capability preservation was not evaluated. No external audit was performed. "
       "The primary holdout remains sealed. No model checkpoint is recommended for release.")
desc=("<p>We tested one frozen character post-training recipe across three model families. "
      "It reduced unsupported assertions, but no family preserved grounded-answer accuracy "
      "well enough to meet the pre-registered bar.</p>"
      f"<p><strong>Scope.</strong> {scope}</p>"
      "<p>This is an aggregate-only release. It does not contain item-level scored outputs, "
      "judge ledgers, benchmark prompt text, model weights, or the primary-test holdout, and "
      "does not support independent recomputation of the readout. See Appendix D of the report.</p>")
print(json.dumps({"metadata":{
 "upload_type":"publication","publication_type":"report",
 "title":("Character Transfer Across Three Model Families: Reduced unsupported assertions, "
          "impaired grounded answering, and a failed utility-preservation bar"),
 "creators":[{"name":"Pu, George","affiliation":"SimpleDirect / Vinci Research"},
             {"name":"Naik, Ayush","affiliation":"SimpleDirect / Vinci Research"}],
 "description":desc,"publication_date":"2026-09-01","version":"1.0",
 "language":"eng","access_right":"open","license":"cc-by-4.0",
 "keywords":["character post-training","Direct Preference Optimization","unsupported assertions",
             "answer preservation","cross-family transfer","LLM-as-a-judge",
             "evaluation reliability","negative result"],
 "related_identifiers":[{"identifier":url,"relation":"isIdenticalTo","scheme":"url"}],
 "notes":scope}},indent=2))
PY
api PUT "$API/deposit/depositions/$DEP_ID" -H "Content-Type: application/json" -d @"$BODY.meta" >/dev/null
rm -f "$BODY.meta"; ok "metadata written"

echo "== 6. verify the end state =="
api GET "$API/deposit/depositions/$DEP_ID" | jq_py "
m=d['metadata']; files={f['filename']:f['checksum'] for f in d.get('files',[])}
print('  state    :', d.get('state'), ' submitted:', d.get('submitted'))
print('  version  :', m.get('version'), ' licence:', m.get('license'))
for k,v in files.items(): print('  file     :', k, v)
ok = (not d.get('submitted')
      and m.get('version')=='1.0'
      and 'No model checkpoint is recommended for release' in (m.get('description') or '')
      and len(files)==2)
print('  scope line in description:', 'No model checkpoint is recommended for release' in (m.get('description') or ''))
print('  >>>', 'STAGED CORRECTLY' if ok else 'CHECK THE ABOVE — something is off')
"
echo
echo "Staged, NOT published. Review then publish by hand:"
echo "  https://zenodo.org/uploads/$DEP_ID"
