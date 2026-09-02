#!/usr/bin/env bash
# The private-use gate, closed by a pair: the same checker, the same entry
# point, two PDFs differing only in their ToUnicode mapping.
#
# Without the positive case a checker that refused everything would look
# identical to a working one.
set -uo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
fails=0
ck() { # name expected_exit file
  python3 scripts/pdf_text_sanity.py "$3" >/dev/null 2>&1; got=$?
  if [ "$got" = "$2" ]; then printf '  PASS   %-46s exit=%s\n' "$1" "$got"
  else printf '  FAIL   %-46s exit=%s want=%s\n' "$1" "$got" "$2"; fails=$((fails+1)); fi
}
python3 test/make_pua_pdf.py "$TMP/clean.pdf"
python3 test/make_pua_pdf.py "$TMP/pua.pdf" --pua

ck "negative: private-use code point rejected"   1 "$TMP/pua.pdf"
ck "positive: ordinary text accepted"            0 "$TMP/clean.pdf"

# The defect is invisible on the page: both fixtures draw the same bytes, so a
# visual check cannot separate them and only extraction can.
a=$(pdftotext "$TMP/clean.pdf" - | tr -d '[:space:]')
b=$(pdftotext "$TMP/pua.pdf"   - | tr -d '[:space:]')
if [ "$a" = "$b" ]; then printf '  FAIL   fixtures extract identically — not discriminating\n'; fails=$((fails+1))
else printf '  PASS   %-46s "%s" vs "%s"\n' "extraction differs, as the defect requires" "$a" "$b"; fi

# A missing file must fail, not pass by producing no text.
ck "absent file rejected, not silently clean"    2 "$TMP/nope.pdf"

[ "$fails" = 0 ] && echo "  pua-gate: all cases passed" || { echo "  pua-gate: $fails FAILED"; exit 1; }
