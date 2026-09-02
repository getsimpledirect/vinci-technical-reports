#!/usr/bin/env bash
# Exercise the PDF_FORBID_URI gate in assemble_release.sh. Publishes nothing.
#
# The gate must fail for its OWN reason, so both cases use the SAME real PDF and
# a config whose text gates all pass on it. Only PDF_FORBID_URI differs. If an
# earlier REQUIRE/FORBID gate answered first, the negative case would go green
# without the URI gate ever running.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF="${1:-$HOME/Downloads/Vinci_TR3_Runtime_Pass_Is_Not_Correctness_v1.0.1/report/Vinci_Technical_Report_No_3_v1.0.pdf}"
[ -f "$PDF" ] || { echo "SKIP: fixture PDF not found: $PDF"; exit 0; }

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo/scripts" "$TMP/repo/reports/fixture"
# Copy EVERY script assemble_release.sh calls. It gained an unconditional
# pdf_text_sanity.py check; omitting it made this suite fail in the earlier
# gate instead of the one under test, which reads as a URI-gate regression.
cp "$ROOT/scripts/assemble_release.sh" "$ROOT/scripts/pdf_uris.py" \
   "$ROOT/scripts/pdf_text_sanity.py" "$TMP/repo/scripts/"

conf(){ cat > "$TMP/repo/reports/fixture/release.conf" <<EOF
REPORT_TITLE="fixture"; REPORT_NUMBER="fixture"; VERSION="1.0"; PUB_DATE="2026-09-01"
PDF_NAME="f.pdf"; ZIP_BASE="fixture-public"; ZENODO_DEP_ID=""; DOI=""; REPORT_URL=""
PDF_REQUIRE_REGEX=( "Runtime Pass Is Not Correctness" )
PDF_FORBID=( "string-not-in-this-pdf-zzz" )
MIN_PAGES=30
PDF_FORBID_URI=( $1 )
LICENSE_ID="cc-by-4.0"; ZENODO_SCOPE=""; SCOPE_PROBE=""; ZENODO_KEYWORDS='[]'
EOF
}
run(){ bash "$TMP/repo/scripts/assemble_release.sh" fixture "$PDF" 2>&1; }
fails=0
say(){ printf '  %-6s %-42s %s\n' "$1" "$2" "$3"; [ "$1" = FAIL ] && fails=$((fails+1)); return 0; }

# NEGATIVE: the PDF links to vinci-gpu-research -> gate must reject, by name.
conf '"vinci-gpu-research"'; OUT="$(run)"
grep -q "forbidden target" <<<"$OUT" \
  && say PASS "negative: forbidden link target rejected" "gate fired" \
  || say FAIL "negative: forbidden link target rejected" "$(head -3 <<<"$OUT"|tr '\n' ' ')"

# POSITIVE REACHABILITY: same PDF, same path, a pattern it does not contain.
# The gate must RUN and pass -- proving the negative was not a blanket refusal.
conf '"no-such-host-xyzzy"'; OUT="$(run)"
grep -q "no forbidden link targets" <<<"$OUT" \
  && say PASS "positive: gate runs and passes" "reachable" \
  || say FAIL "positive: gate runs and passes" "$(head -3 <<<"$OUT"|tr '\n' ' ')"
grep -q "forbidden target" <<<"$OUT" \
  && say FAIL "positive: must not reject" "rejected anyway" \
  || say PASS "positive: must not reject" "clean"

echo; [ "$fails" -eq 0 ] && echo "  uri-gate: all cases passed" || echo "  uri-gate: $fails FAILED"
exit "$fails"
