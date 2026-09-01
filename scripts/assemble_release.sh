#!/usr/bin/env bash
# Finish the TR2 v1.0 release once the archival PDF exists.
#
#   ./scripts/assemble_release.sh /path/to/Vinci_Technical_Report_No_2.pdf
#
# Verifies the PDF, installs it, regenerates the manifest LAST, checks the
# manifest covers the tree, then builds the public ZIP and its detached
# checksum. Creates no tag, publishes nothing, changes no visibility.
set -euo pipefail

PDF="${1:?usage: assemble_release.sh /path/to/Vinci_Technical_Report_No_2.pdf}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PKG="$ROOT/reports/tr2"
DIST="$ROOT/dist"
NAME="Vinci-TR2-Character-Transfer-v1.0-public"

fail(){ echo "  FAIL: $*" >&2; exit 1; }
ok(){   echo "  ok   $*"; }

echo "== 1. verify the PDF before it goes anywhere =="
[ -f "$PDF" ] || fail "no such file: $PDF"
command -v pdftotext >/dev/null || fail "pdftotext not found (brew install poppler)"
TXT="$(mktemp)"; pdftotext "$PDF" "$TXT"
PAGES=$(pdfinfo "$PDF" | awk '/^Pages:/{print $2}')
[ "${PAGES:-0}" -ge 8 ] || fail "only ${PAGES:-0} pages; expected 8 or more"
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
grep -qE "Version 1\.0 (-|\xe2\x80\xa2|.) 1 September 2026" "$TXT" \
  || fail 'title block does not read "Version 1.0 <sep> 1 September 2026"'
ok 'title block is the v1.0 line'
grep -q "Outstanding Evidence Work" "$TXT" || fail 'Appendix D is not the v1.0 "Outstanding Evidence Work"'
ok 'Appendix D is the v1.0 text'
grep -q "10.5281/zenodo.22236690" "$TXT" || echo "  WARN the DOI does not appear in the PDF text"
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

echo "== 2. install it and drop the placeholder =="
cp "$PDF" "$PKG/report/Vinci_Technical_Report_No_2.pdf"; ok "installed into reports/tr2/report/"
rm -f "$PKG/report/PDF_NOT_BUILT.md";                    ok "removed PDF_NOT_BUILT.md"

echo "== 3. manifest LAST, then prove it covers the tree =="
( cd "$PKG" && python3 source/build_manifest.py >/dev/null )
( cd "$PKG" && python3 - <<'PY'
import json,os,sys
m=json.load(open('manifest.json')); listed={f['path'] for f in m['files']}
actual={os.path.relpath(os.path.join(r,f),'.') for r,d,fs in os.walk('.') for f in fs}
extra=actual-listed-{'manifest.json','checksums.sha256'}; missing=listed-actual
if extra or missing:
    print(f"  FAIL uncovered={sorted(extra)} phantom={sorted(missing)}"); sys.exit(1)
print(f"  ok   manifest {m['file_count']} + 2 == {len(actual)} on disk, nothing uncovered")
PY
) || fail "manifest does not cover the tree"
( cd "$PKG" && shasum -a 256 -c checksums.sha256 >/dev/null ) && ok "all checksums verify"

echo "== 4. public ZIP and detached checksum =="
mkdir -p "$DIST"; rm -f "$DIST/$NAME.zip" "$DIST/$NAME.zip.sha256"
( cd "$PKG/.." && zip -qr "$DIST/$NAME.zip" "tr2" -x '*.DS_Store' )
( cd "$DIST" && shasum -a 256 "$NAME.zip" > "$NAME.zip.sha256" )
ok "dist/$NAME.zip  ($(du -h "$DIST/$NAME.zip" | cut -f1))"
( cd "$DIST" && shasum -a 256 -c "$NAME.zip.sha256" >/dev/null ) && ok "detached checksum verifies"

echo
echo "Assembled. Nothing was published, tagged, or made public."
echo "ZIP sha256: $(awk '{print $1}' "$DIST/$NAME.zip.sha256")"
echo "Next: RELEASE_RUNBOOK.md, starting at step 3."
