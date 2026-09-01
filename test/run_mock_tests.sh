#!/usr/bin/env bash
# Exercise zenodo_stage.sh against a mock Zenodo. Never touches zenodo.org.
# Uses the PRODUCTION basenames, so the same-key collision that made 23187b7
# unsafe actually occurs. Exits non-zero if any case fails.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP=$(mktemp -d)
MOCK_PID=""
cleanup(){ [ -n "$MOCK_PID" ] && kill "$MOCK_PID" 2>/dev/null; rm -rf "$TMP"; }
trap cleanup EXIT

# Production basenames. With any other name the bucket key does not collide and
# the stable-id case cannot be reproduced — the first version of this harness
# used tr2.pdf and silently tested nothing.
PDF_NAME=Vinci_Technical_Report_No_2.pdf
ZIP_NAME=Vinci-TR2-Character-Transfer-v1.0-public.zip
python3 "$ROOT/test/make_test_pdf.py" "$TMP/$PDF_NAME"
head -c 4096 /dev/urandom > "$TMP/$ZIP_NAME"
[ -s "$TMP/$PDF_NAME" ] || { echo "could not synthesise a test PDF"; exit 1; }

FAILURES=0
start_mock(){ [ -n "$MOCK_PID" ] && kill "$MOCK_PID" 2>/dev/null; sleep 0.3
  { ZENODO_ALLOW_HOST=127.0.0.1 python3 "$ROOT/test/mock_zenodo.py" --port 8899 "$@" >/dev/null 2>&1 & MOCK_PID=$!; } 2>/dev/null; disown 2>/dev/null; sleep 0.8; }
files_now(){ curl -s -H "Authorization: Bearer mock" \
  http://127.0.0.1:8899/api/deposit/depositions/22236690 \
  | python3 -c "import json,sys;print(','.join(sorted(f['filename'] for f in json.load(sys.stdin)['files'])))"; }
invoke(){ sed -e "s#^API=.*#API=http://127.0.0.1:8899/api#" \
              -e "s#^PDF=.*#PDF=$TMP/$PDF_NAME#" -e "s#^ZIP=.*#ZIP=$TMP/$ZIP_NAME#" "$1" > "$TMP/s.sh"
          ZENODO_ALLOW_HOST="${ZENODO_ALLOW_HOST-127.0.0.1}" ZENODO_TOKEN=mock ZENODO_TOKEN_FILE=/nonexistent bash "$TMP/s.sh" >"$TMP/out" 2>&1; echo $?; }
check(){ # check <label> <actual> <expected>
  if [ "$2" = "$3" ]; then printf '  PASS  %-46s %s\n' "$1" "$2"
  else printf '  FAIL  %-46s got %s want %s\n' "$1" "$2" "$3"; FAILURES=$((FAILURES+1)); sed 's/^/        /' "$TMP/out" | tail -6; fi; }

echo "########## MOCK TESTS (production basenames) ##########"

start_mock --id-stable
check "current: id-stable overwrite, exit"   "$(invoke "$ROOT/scripts/zenodo_stage.sh")" "0"
check "current: both files survive"          "$(files_now)" "$ZIP_NAME,$PDF_NAME"

start_mock
check "current: id-changes overwrite, exit"  "$(invoke "$ROOT/scripts/zenodo_stage.sh")" "0"
check "current: both files survive"          "$(files_now)" "$ZIP_NAME,$PDF_NAME"

start_mock --publish-midrun
check "current: published mid-run refuses"   "$(invoke "$ROOT/scripts/zenodo_stage.sh")" "1"

start_mock --corrupt-upload
check "current: corrupted upload refuses"    "$(invoke "$ROOT/scripts/zenodo_stage.sh")" "1"


# --- wrong deposition: identity gate must stop it before ANY write ---
start_mock --dep-id 99999999
rc=$(invoke "$ROOT/scripts/zenodo_stage.sh")
check "wrong deposition id refuses" "$rc" "1"
check "  ...and uploaded nothing"   "$(files_now)" "$PDF_NAME"

start_mock --doi 10.5281/zenodo.00000000
rc=$(invoke "$ROOT/scripts/zenodo_stage.sh")
check "wrong reserved DOI refuses"  "$rc" "1"
check "  ...and uploaded nothing"   "$(files_now)" "$PDF_NAME"

# --- a file we did not put there: must refuse, and must not DELETE ---
start_mock --extra-file
rc=$(invoke "$ROOT/scripts/zenodo_stage.sh")
check "unexpected third file refuses" "$rc" "1"
check "  ...stranger file untouched"  "$(files_now | tr ',' '\n' | grep -c someone_elses_notes.txt)" "1"
check "  ...zero DELETE verbs issued" "$(grep -c 'api DELETE' "$ROOT/scripts/zenodo_stage.sh")" "0"

# --- bucket host must be validated, not substring-matched ---
start_mock
rc=$(ZENODO_ALLOW_HOST= invoke "$ROOT/scripts/zenodo_stage.sh")
check "foreign bucket host refuses"   "$rc" "1"
check "  ...and uploaded nothing"     "$(files_now)" "$PDF_NAME"

# Regression control: the old script must LOSE the PDF here. If this stops
# failing, the harness has stopped reproducing the defect and proves nothing.
if git -C "$ROOT" cat-file -e 23187b7:scripts/zenodo_stage.sh 2>/dev/null; then
  git -C "$ROOT" show 23187b7:scripts/zenodo_stage.sh > "$TMP/old.sh"
  # 23187b7 gates on the hyphen form. Feed it a hyphen PDF, or it aborts at the
  # title check and never reaches the delete bug this control must reproduce.
  python3 "$ROOT/test/make_test_pdf.py" "$TMP/$PDF_NAME" "-"
  start_mock --id-stable
  invoke "$TMP/old.sh" >/dev/null
  got=$(files_now)
  if [ "$got" = "$ZIP_NAME" ]; then
    printf '  PASS  %-46s old script lost the PDF, as it must\n' "control: 23187b7 reproduces the defect"
  else
    printf '  FAIL  %-46s got %s — harness no longer reproduces the bug\n' "control: 23187b7 reproduces the defect" "$got"
    FAILURES=$((FAILURES+1))
  fi
fi

echo
if [ "$FAILURES" -eq 0 ]; then echo "all cases passed"; else echo "$FAILURES case(s) FAILED"; fi
exit $((FAILURES > 0 ? 1 : 0))
