#!/usr/bin/env bash
# Exercise the PDF_FORBID_URI gate in assemble_release.sh. Publishes nothing.
#
# The gate must fail for its OWN reason, so the negative and the reachability
# case use the SAME PDF and a config whose text gates all pass on it. Only
# PDF_FORBID_URI differs. If an earlier REQUIRE/FORBID gate answered first, the
# negative case would go green without the URI gate ever running.
#
# The negative case needs a PDF that actually carries the forbidden link. The
# repaired report PDFs no longer do -- that was the repair -- so a real report
# PDF cannot restore the defect: run against one, the "negative" case failed
# for lack of a fixture, not because the gate was wrong (review R9, 2026-09-02).
# The defect is restored by a generated fixture (test/make_uri_pdf.py) whose
# /URI annotations are the only thing under test. The same fixture then proves
# the gate runs and passes on a pattern it does not carry. Finally the real
# report PDFs must pass the PRODUCTION pattern from reports/tr3/release.conf
# through the same entry point: the repaired artifacts do not link the private
# repository. Pass a PDF path to use it for that third case instead.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/repo/scripts" "$TMP/repo/reports/fixture"
# Copy EVERY script assemble_release.sh calls. It gained an unconditional
# pdf_text_sanity.py check; omitting it made this suite fail in the earlier
# gate instead of the one under test, which reads as a URI-gate regression.
cp "$ROOT/scripts/assemble_release.sh" "$ROOT/scripts/pdf_uris.py" \
   "$ROOT/scripts/pdf_text_sanity.py" "$TMP/repo/scripts/"

FORBIDDEN_URI="https://github.com/getsimpledirect/vinci-gpu-research/tree/main/p-breve-01-r2"
ALLOWED_URI="https://www.getsimpledirect.com/research/papers/runtime-pass-is-not-correctness"
FIXTURE="$TMP/fixture.pdf"
python3 "$ROOT/test/make_uri_pdf.py" "$FIXTURE" "$FORBIDDEN_URI" "$ALLOWED_URI" \
  || { echo "  FAIL: could not generate the fixture PDF"; exit 1; }

# The production pattern, read from the real config rather than retyped here, so
# this suite cannot drift from what assembly actually enforces.
PROD_PATTERN="$(bash -c 'source "$1"; printf "%s" "${PDF_FORBID_URI[0]-}"' _ "$ROOT/reports/tr3/release.conf")"

conf(){ # $1 = PDF_FORBID_URI entries (shell-quoted), $2 = MIN_PAGES
cat > "$TMP/repo/reports/fixture/release.conf" <<EOF
REPORT_TITLE="fixture"; REPORT_NUMBER="fixture"; VERSION="1.0"; PUB_DATE="2026-09-01"
PDF_NAME="f.pdf"; ZIP_BASE="fixture-public"; ZENODO_DEP_ID=""; DOI=""; REPORT_URL=""
PDF_REQUIRE_REGEX=( "Runtime Pass Is Not Correctness" )
PDF_FORBID=( "string-not-in-this-pdf-zzz" )
MIN_PAGES=$2
PDF_FORBID_URI=( $1 )
LICENSE_ID="cc-by-4.0"; ZENODO_SCOPE=""; SCOPE_PROBE=""; ZENODO_KEYWORDS='[]'
EOF
}
run(){ bash "$TMP/repo/scripts/assemble_release.sh" fixture "$1" 2>&1; }
fails=0
say(){ printf '  %-6s %-52s %s\n' "$1" "$2" "$3"; [ "$1" = FAIL ] && fails=$((fails+1)); return 0; }

# FIXTURE VALIDITY: the defect is really present, as a link target, and the
# same extractor the gate uses can see it. Without this the negative case could
# fire on something other than the annotation.
URIS="$(python3 "$TMP/repo/scripts/pdf_uris.py" "$FIXTURE")"
grep -qF "$FORBIDDEN_URI" <<<"$URIS" && grep -qF "$ALLOWED_URI" <<<"$URIS" \
  && say PASS "fixture: forbidden + allowed link targets extracted" "$(grep -c . <<<"$URIS") link(s)" \
  || say FAIL "fixture: forbidden + allowed link targets extracted" "$(tr '\n' ' ' <<<"$URIS")"
pdftotext "$FIXTURE" - 2>/dev/null | grep -q "vinci-gpu-research" \
  && say FAIL "fixture: target absent from extracted TEXT" "text-level gate could see it; not discriminating" \
  || say PASS "fixture: target absent from extracted TEXT" "only the annotation carries it"

# NEGATIVE: the fixture links to vinci-gpu-research -> gate must reject, by name,
# and it must be the ONLY refusal: every gate ahead of it passed.
conf '"vinci-gpu-research"' 1; OUT="$(run "$FIXTURE")"
grep -q 'forbidden target matching "vinci-gpu-research"' <<<"$OUT" \
  && say PASS "negative: forbidden link target rejected" "gate fired" \
  || say FAIL "negative: forbidden link target rejected" "$(head -3 <<<"$OUT"|tr '\n' ' ')"
[ "$(grep -c 'FAIL' <<<"$OUT")" = 1 ] && grep -q "free of private-use code points" <<<"$OUT" \
  && say PASS "negative: earlier gates passed; URI gate is the refusal" "one FAIL line" \
  || say FAIL "negative: earlier gates passed; URI gate is the refusal" "$(grep FAIL <<<"$OUT"|tr '\n' ' ')"

# POSITIVE REACHABILITY: same PDF, same path, a pattern it does not contain.
# The gate must RUN and pass -- proving the negative was not a blanket refusal.
conf '"no-such-host-xyzzy"' 1; OUT="$(run "$FIXTURE")"
grep -q "no forbidden link targets (1 pattern(s), 2 link(s) scanned)" <<<"$OUT" \
  && say PASS "positive: gate runs and passes on the same fixture" "reachable, 2 links scanned" \
  || say FAIL "positive: gate runs and passes on the same fixture" "$(head -3 <<<"$OUT"|tr '\n' ' ')"
grep -q "forbidden target" <<<"$OUT" \
  && say FAIL "positive: must not reject" "rejected anyway" \
  || say PASS "positive: must not reject" "clean"

# REPAIRED ARTIFACTS: the real report PDFs, the PRODUCTION pattern, the same
# entry point. This is the repair the gate exists to hold: neither PDF links
# the private repository any more.
if [ -z "$PROD_PATTERN" ]; then
  say FAIL "repaired: production PDF_FORBID_URI read from release.conf" "empty"
else
  say PASS "repaired: production PDF_FORBID_URI read from release.conf" "\"$PROD_PATTERN\""
  if [ $# -ge 1 ]; then REAL=("$1"); else
    REAL=("$ROOT/reports/tr3/report/Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf"
          "$ROOT/reports/tr3/report/Vinci_Technical_Report_No_3_v1.0.pdf")
  fi
  for pdf in "${REAL[@]}"; do
    name="$(basename "$pdf")"
    [ -f "$pdf" ] || { say FAIL "repaired: $name" "not found"; continue; }
    conf "\"$PROD_PATTERN\"" 30; OUT="$(run "$pdf")"
    grep -q "no forbidden link targets" <<<"$OUT" && ! grep -q "forbidden target" <<<"$OUT" \
      && say PASS "repaired: $name passes the production pattern" "$(grep -o '[0-9]* link(s) scanned' <<<"$OUT")" \
      || say FAIL "repaired: $name passes the production pattern" "$(grep 'FAIL\|forbidden' <<<"$OUT"|head -2|tr '\n' ' ')"
  done
fi

echo; [ "$fails" -eq 0 ] && echo "  uri-gate: all cases passed" || echo "  uri-gate: $fails FAILED"
exit "$fails"
