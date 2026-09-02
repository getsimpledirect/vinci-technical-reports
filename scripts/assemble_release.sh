#!/usr/bin/env bash
# Assemble one configured report once its archival PDF exists.
#
#   ./scripts/assemble_release.sh <report-slug> /path/to/report.pdf
#
# Report-specific values live in reports/<slug>/release.conf. This script holds
# none: adding a report means adding a config, not editing logic here.
#
# Verifies the PDF, installs it, regenerates derivatives and the manifest LAST,
# re-verifies that the PDF the rebuild left in the tree still carries the gated
# digest, checks the manifest covers the tree, then builds the public ZIP and its
# detached checksum. Creates no tag, publishes nothing, changes no visibility.
set -euo pipefail

SLUG="${1:?usage: assemble_release.sh <report-slug> /path/to/report.pdf}"
PDF="${2:?usage: assemble_release.sh <report-slug> /path/to/report.pdf}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKG="$ROOT/reports/$SLUG"
CONF="$PKG/release.conf"
[ -r "$CONF" ] || { echo "  FAIL: no release.conf at $CONF" >&2; exit 1; }
# shellcheck disable=SC1090
source "$CONF"
VERSION="${REPORT_VERSION:-${VERSION:-}}"
MANIFEST_FILE="${MANIFEST_FILE:-manifest.json}"
CHECKSUM_FILE="${CHECKSUM_FILE:-checksums.sha256}"
PACKAGE_DIR_NAME="${PACKAGE_DIR_NAME:-$SLUG}"
DIST="$ROOT/dist"
NAME="$ZIP_BASE"

fail(){ echo "  FAIL: $*" >&2; exit 1; }
ok(){   echo "  ok   $*"; }

# A refusal anywhere below must leave NO archive behind, including one from an
# earlier run of this script, so a stale dist/ ZIP can never be mistaken for the
# output of a run that was refused.
rm -f "$DIST/$NAME.zip" "$DIST/$NAME.zip.sha256"

echo "== 1. verify the PDF before it goes anywhere =="
[ -f "$PDF" ] || fail "no such file: $PDF"
EXPECTED_PDF_SHA256="${ASSEMBLY_PDF_SHA256:-${ACCEPTED_PDF_SHA256:-}}"
PDF_SHA="$(shasum -a 256 "$PDF" | awk '{print $1}')"
if [ -n "$EXPECTED_PDF_SHA256" ]; then
  [ "$PDF_SHA" = "$EXPECTED_PDF_SHA256" ] || fail "PDF digest $PDF_SHA is not the configured assembly digest $EXPECTED_PDF_SHA256"
elif [ -e "$PKG/source/rebuild_all.sh" ]; then
  # A package that rebuilds its PDF from source can only be approved by a
  # digest: without one, the post-rebuild check below compares the rebuilt
  # bytes against whatever was handed in, which proves self-consistency and
  # approves nothing (review R13, finding N1). Refuse before any gate runs.
  fail "no ASSEMBLY_PDF_SHA256 configured in $CONF; nothing approves these bytes. reports/$SLUG has a rebuild path (source/rebuild_all.sh), so the supplied PDF cannot stand in for an approved digest. Review the candidate and record its sha256 as ASSEMBLY_PDF_SHA256 in release.conf. No archive was written."
fi
# The digest every later step must still see. Only a package with NO rebuild
# path (the PDF is supplied, never regenerated, so the manifest step cannot
# replace it) may proceed on the supplied bytes alone.
GATED_PDF_SHA256="${EXPECTED_PDF_SHA256:-$PDF_SHA}"
command -v pdftotext >/dev/null || fail "pdftotext not found (brew install poppler)"
TXT="$(mktemp)"; pdftotext "$PDF" "$TXT"
PAGES=$(pdfinfo "$PDF" | awk '/^Pages:/{print $2}')
[ "${PAGES:-0}" -ge "${MIN_PAGES:-8}" ] || fail "only ${PAGES:-0} pages; expected ${MIN_PAGES:-8} or more"
ok "$PAGES pages"
# Presence of "Version 1.0" is NOT a usable gate: the v0.9 draft contains that
# string inside the old appendix title "Publication Corrections Required Before
# Version 1.0". Gate on the draft markers being ABSENT instead.
grep -q "Version 0.9"                                        "$TXT" && fail 'PDF contains "Version 0.9" — this is the draft'
grep -q "publication draft"                                  "$TXT" && fail 'PDF says "publication draft" — this is the draft'
grep -q "Publication Corrections Required Before Version 1.0" "$TXT" && fail 'PDF carries the old Appendix D — this is the draft'
ok 'no draft markers present'
# The template prints "Version 1.0 <bullet> 1 September 2026". Gating on a
# hyphen rejected the real PDF while passing nothing — match the separator the
# template actually emits, and tolerate either.
for s in ${PDF_FORBID[@]+"${PDF_FORBID[@]}"}; do   # empty-array safe (bash 3.2 + set -u)
  grep -qF "$s" "$TXT" && fail "PDF contains \"$s\" -- this looks like a draft, not the final build"
done
ok "no draft markers (${#PDF_FORBID[@]} checked)"
# Required phrases match against a whitespace-flattened copy: a designed cover
# wraps the title across lines, and grep cannot match a newline inside a bracket
# expression, so gating on the one-line form rejects a correct PDF.
FLAT="$(mktemp)"; tr '\n' ' ' < "$TXT" | tr -s ' ' > "$FLAT"
for r in ${PDF_REQUIRE_REGEX[@]+"${PDF_REQUIRE_REGEX[@]}"}; do
  grep -qE "$r" "$FLAT" || fail "PDF is missing required content: /$r/"
done
ok "all ${#PDF_REQUIRE_REGEX[@]} required strings present"
# Private-use code points. Unconditional: a glyph with no meaning outside the
# font that emitted it has no place in an archival PDF, and this failure is
# invisible on the page -- only extraction is wrong. See scripts/pdf_text_sanity.py.
python3 "$(dirname "$0")/pdf_text_sanity.py" "$PDF" \
  || fail "PDF extraction contains private-use code points (signs or identifiers will be lost downstream)"
ok "extracted text is free of private-use code points"
# Link targets, not link text. pdftotext yields only a hyperlink's visible
# label, so a forbidden URL can sit in the PDF and never appear in "$TXT".
# Reports needing this declare PDF_FORBID_URI; those that do not are unaffected.
if declare -p PDF_FORBID_URI >/dev/null 2>&1 && [ "${#PDF_FORBID_URI[@]}" -gt 0 ]; then
  URIS="$(python3 "$(dirname "$0")/pdf_uris.py" "$PDF")"
  for u in ${PDF_FORBID_URI[@]+"${PDF_FORBID_URI[@]}"}; do
    grep -q "$u" <<<"$URIS" && fail "PDF links to a forbidden target matching \"$u\""
  done
  ok "no forbidden link targets (${#PDF_FORBID_URI[@]} pattern(s), $(grep -c . <<<"$URIS") link(s) scanned)"
fi
grep -qF "$DOI" "$TXT" || echo "  WARN the DOI $DOI does not appear in the PDF text"
if pdffonts "$PDF" | tail -n +3 | awk '$0!=""{if($(NF-3)!="yes") bad=1} END{exit bad?1:0}'; then
  ok "all fonts embedded"; else fail "a font is not embedded"; fi
LINKS=$(python3 - "$PDF" <<'PY'
import sys
try:
    from pypdf import PdfReader
    print(sum(len(p.get('/Annots') or []) for p in PdfReader(sys.argv[1]).pages))
except Exception: print(-1)
PY
)
if   [ "$LINKS" -gt 0 ]; then ok "$LINKS link annotations (autolink_bare_uris worked)"
elif [ "$LINKS" -eq 0 ]; then echo "  WARN zero link annotations — was autolink_bare_uris passed to pandoc?"
else echo "  note link check skipped (pypdf not installed)"; fi

echo "== 2. install the configured assembly PDF and drop the placeholder =="
TARGET_PDF="$PKG/report/${ASSEMBLY_PDF_NAME:-$PDF_NAME}"
if [ "$(cd "$(dirname "$PDF")" && pwd)/$(basename "$PDF")" != "$(cd "$(dirname "$TARGET_PDF")" && pwd)/$(basename "$TARGET_PDF")" ]; then
  cp "$PDF" "$TARGET_PDF"
fi
ok "configured assembly PDF present in reports/$SLUG/report/"
rm -f "$PKG/report/PDF_NOT_BUILT.md";                    ok "removed PDF_NOT_BUILT.md (if present)"

echo "== 3. manifest LAST, then prove it covers the tree =="
( cd "$PKG" && if [ -x source/rebuild_all.sh ] && [ -f source/package_release.py ]; then bash source/rebuild_all.sh --write >/dev/null; else python3 source/build_manifest.py >/dev/null; fi )
# The rebuild regenerates the candidate PDF from the canonical manuscript and can
# overwrite the file verified in step 1. Step 1 gated the bytes that were handed
# in; the archive carries the bytes that are in the tree NOW. Gate those. If the
# manuscript drifted from the approved candidate, the rebuilt PDF differs, and
# packaging it would ship bytes nobody approved under a digest that no longer
# describes them. Refuse before any ZIP is written (step 4 is the only writer).
POST_PDF_SHA="$(shasum -a 256 "$TARGET_PDF" | awk '{print $1}')"
[ "$POST_PDF_SHA" = "$GATED_PDF_SHA256" ] || fail "rebuild changed the assembly PDF: $TARGET_PDF is now $POST_PDF_SHA, not the gated $GATED_PDF_SHA256. The tree now holds regenerated derivatives; review them and re-approve a new digest in release.conf, or restore the tree. No archive was written."
ok "assembly PDF unchanged by rebuild ($POST_PDF_SHA)"
( cd "$PKG" && MANIFEST_FILE="$MANIFEST_FILE" CHECKSUM_FILE="$CHECKSUM_FILE" python3 - <<'PY'
import json,os,sys
manifest=os.environ['MANIFEST_FILE']; checksums=os.environ['CHECKSUM_FILE']
m=json.load(open(manifest)); listed={f['path'] for f in m['files']}
actual={os.path.relpath(os.path.join(r,f),'.') for r,d,fs in os.walk('.') for f in fs}
extra=actual-listed-{manifest,checksums}; missing=listed-actual
if extra or missing:
    print(f"  FAIL uncovered={sorted(extra)} phantom={sorted(missing)}"); sys.exit(1)
print(f"  ok   manifest {m['file_count']} + 2 == {len(actual)} on disk, nothing uncovered")
PY
) || fail "manifest does not cover the tree"
( cd "$PKG" && shasum -a 256 -c "$CHECKSUM_FILE" >/dev/null ) && ok "all checksums verify"

echo "== 4. public ZIP and detached checksum =="
mkdir -p "$DIST"; rm -f "$DIST/$NAME.zip" "$DIST/$NAME.zip.sha256"
( cd "$PKG" && PACKAGE_DIR_NAME="$PACKAGE_DIR_NAME" python3 - "$DIST/$NAME.zip" <<'PY'
import os,pathlib,stat,sys,zipfile
root=pathlib.Path('.'); target=pathlib.Path(sys.argv[1]); prefix=os.environ['PACKAGE_DIR_NAME']
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(x for x in root.rglob('*') if x.is_file() and x.name != '.DS_Store'):
        info=zipfile.ZipInfo(f"{prefix}/{p.as_posix()}",(2026,9,1,0,0,0))
        info.external_attr=(p.stat().st_mode & 0xffff)<<16; info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
PY
)
( cd "$DIST" && shasum -a 256 "$NAME.zip" > "$NAME.zip.sha256" )
ok "dist/$NAME.zip  ($(du -h "$DIST/$NAME.zip" | cut -f1))"
( cd "$DIST" && shasum -a 256 -c "$NAME.zip.sha256" >/dev/null ) && ok "detached checksum verifies"

echo
echo "Assembled. Nothing was published, tagged, or made public."
echo "ZIP sha256: $(awk '{print $1}' "$DIST/$NAME.zip.sha256")"
echo "Next: review the generated archive and request separate authority for any publication action."
