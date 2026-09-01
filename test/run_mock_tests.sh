#!/usr/bin/env bash
# Exercise zenodo_stage.sh against a mock, including the failure that made the
# previous version unsafe. Never touches zenodo.org.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"; pkill -f mock_zenodo.py 2>/dev/null || true' EXIT

# stand-in artifacts that satisfy the v1.0 content gates
python3 "$ROOT/test/make_test_pdf.py" "$TMP/tr2.pdf"
[ -s "$TMP/tr2.pdf" ] || { echo "could not synthesise a test PDF"; exit 1; }
head -c 4096 /dev/urandom > "$TMP/pkg.zip"

run_case(){ # run_case <name> <mock flags...> ; echoes PASS/FAIL
  local name="$1"; shift
  pkill -f mock_zenodo.py 2>/dev/null; sleep 0.4
  python3 "$ROOT/test/mock_zenodo.py" --port 8899 "$@" >/dev/null 2>&1 &
  sleep 0.8
  sed -e "s#^API=.*#API=http://127.0.0.1:8899/api#" \
      -e "s#^PDF=.*#PDF=$TMP/tr2.pdf#" -e "s#^ZIP=.*#ZIP=$TMP/pkg.zip#" \
      -e "s#^DEP_ID=.*#DEP_ID=22236690#" "$ROOT/scripts/zenodo_stage.sh" > "$TMP/s.sh"
  chmod +x "$TMP/s.sh"
  ZENODO_TOKEN=mock ZENODO_TOKEN_FILE=/nonexistent bash "$TMP/s.sh" > "$TMP/out.$$" 2>&1
  local rc=$?
  echo "$name|$rc|$TMP/out.$$"
}

echo "########## MOCK TESTS ##########"
for spec in \
  "id-changes-on-overwrite (normal):--id-stable-NO:0" \
  "id-STABLE-on-overwrite  (the bug):--id-stable:0" \
  "published mid-run:--publish-midrun:1" \
  "corrupted upload:--corrupt-upload:1" ; do
  IFS=':' read -r name flag want <<< "$spec"
  [ "$flag" = "--id-stable-NO" ] && flag=""
  IFS='|' read -r _ rc outf <<< "$(run_case "$name" $flag)"
  verdict=$([ "$rc" = "$want" ] && echo PASS || echo "FAIL (rc=$rc want=$want)")
  printf '  %-38s %s\n' "$name" "$verdict"
  [ "$verdict" = PASS ] || sed 's/^/      /' "$outf" | tail -8
  # the crucial invariant: after a run, the PDF must still be on the record
  if [ "$want" = "0" ]; then
    left=$(curl -s -H "Authorization: Bearer mock" http://127.0.0.1:8899/api/deposit/depositions/22236690 \
           | python3 -c "import json,sys;print(len(json.load(sys.stdin)['files']))")
    printf '  %-38s files left on record: %s %s\n' "" "$left" "$([ "$left" = 2 ] && echo '(PDF+ZIP, correct)' || echo '<-- FILE LOST')"
  fi
done
