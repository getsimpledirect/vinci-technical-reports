#!/usr/bin/env bash
# Stage the TR2 v1.0 files and metadata onto the reserved Zenodo draft.
#
#   export ZENODO_TOKEN=...          # deposit:write ONLY — see below
#   ./scripts/zenodo_stage.sh
#
# Replaces the staged v0.9 PDF, uploads the public ZIP, and writes the final
# metadata. It DOES NOT PUBLISH, and with a correctly scoped token it cannot:
# publishing requires the deposit:actions scope, which this script never needs.
# Create the token WITHOUT that scope and the irreversible step stays manual.
#
# Publishing is permanent. A published Zenodo record can gain a new version but
# can never lose or replace a file. Publish by hand, in the UI, after review.
set -euo pipefail

DEP_ID=22236690
DOI="10.5281/zenodo.22236690"
API=https://zenodo.org/api
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PDF="$ROOT/reports/tr2/report/Vinci_Technical_Report_No_2.pdf"
ZIP="$ROOT/dist/Vinci-TR2-Character-Transfer-v1.0-public.zip"
URL="https://www.getsimpledirect.com/research/papers/character-transfer-across-three-model-families"

: "${ZENODO_TOKEN:?set ZENODO_TOKEN (scope: deposit:write, NOT deposit:actions)}"
fail(){ echo "  FAIL: $*" >&2; exit 1; }
ok(){ echo "  ok   $*"; }
api(){ curl -sS -H "Authorization: Bearer $ZENODO_TOKEN" "$@"; }

[ -f "$PDF" ] || fail "no v1.0 PDF yet — run assemble_release.sh first"
[ -f "$ZIP" ] || fail "no public ZIP yet — run assemble_release.sh first"

echo "== 0. refuse to stage the draft PDF =="
pdftotext "$PDF" /tmp/z.txt
grep -q "Version 0.9" /tmp/z.txt && fail 'that PDF contains "Version 0.9" — it is the draft'
grep -q "Version 1.0 - 1 September 2026" /tmp/z.txt || fail 'title block is not the v1.0 line'
ok "PDF is the v1.0 build"

echo "== 1. read the draft =="
DEP=$(api "$API/deposit/depositions/$DEP_ID") || fail "cannot read deposition $DEP_ID"
echo "$DEP" | python3 -c "
import json,sys
d=json.load(sys.stdin)
if d.get('submitted'): print('  FAIL: this deposition is already PUBLISHED — stop'); sys.exit(1)
print(f\"  ok   draft, state={d.get('state')}, doi={d.get('metadata',{}).get('prereserve_doi',{}).get('doi') or d.get('doi_url','(reserved)')}\")
for f in d.get('files',[]): print(f\"       existing file: {f['filename']}  {f['checksum']}\")
print(d['links']['bucket'])" > /tmp/zinfo.txt || fail "deposition already published, or unreadable"
sed '$d' /tmp/zinfo.txt; BUCKET=$(tail -1 /tmp/zinfo.txt)

echo "== 2. remove the v0.9 file =="
echo "$DEP" | python3 -c "
import json,sys
for f in json.load(sys.stdin).get('files',[]): print(f['id'],f['filename'])" | while read -r fid fname; do
  api -X DELETE "$API/deposit/depositions/$DEP_ID/files/$fid" >/dev/null && ok "deleted $fname"
done

echo "== 3. upload the v1.0 files =="
for f in "$PDF" "$ZIP"; do
  n=$(basename "$f")
  api -X PUT --upload-file "$f" "$BUCKET/$n" >/dev/null && ok "uploaded $n ($(du -h "$f"|cut -f1))"
done

echo "== 4. write the final metadata =="
python3 - "$DOI" "$URL" > /tmp/zmeta.json <<'PY'
import json,sys
doi,url=sys.argv[1],sys.argv[2]
scope=("Development-tier validation evidence only. Refusal adjustment is Judge-B-only. "
       "Capability preservation was not evaluated. No external audit was performed. "
       "The primary holdout remains sealed. No model checkpoint is recommended for release.")
desc=("<p>We tested one frozen character post-training recipe across three model families. "
      "It reduced unsupported assertions, but no family preserved grounded-answer accuracy "
      "well enough to meet the pre-registered bar.</p>"
      f"<p><strong>Scope.</strong> {scope}</p>"
      "<p>This is an aggregate-only release. It does not contain item-level scored outputs, "
      "judge ledgers, benchmark prompt text, model weights, or the primary-test holdout, and "
      "does not support independent recomputation of the readout. See Appendix D.</p>")
print(json.dumps({"metadata":{
 "upload_type":"publication","publication_type":"report",
 "title":("Character Transfer Across Three Model Families: Reduced unsupported assertions, "
          "impaired grounded answering, and a failed utility-preservation bar"),
 "creators":[{"name":"Pu, George","affiliation":"SimpleDirect / Vinci Research"},
             {"name":"Naik, Ayush","affiliation":"SimpleDirect / Vinci Research"}],
 "description":desc,"publication_date":"2026-09-01","version":"1.0",
 "language":"eng","access_right":"open","license":"cc-by-4.0",
 "keywords":["character post-training","Direct Preference Optimization",
             "unsupported assertions","answer preservation","cross-family transfer",
             "LLM-as-a-judge","evaluation reliability","negative result"],
 "related_identifiers":[{"identifier":url,"relation":"isIdenticalTo","scheme":"url"}],
 "notes":scope}},indent=2))
PY
api -X PUT -H "Content-Type: application/json" \
    -d @/tmp/zmeta.json "$API/deposit/depositions/$DEP_ID" >/dev/null && ok "metadata written"

echo "== 5. confirm =="
api "$API/deposit/depositions/$DEP_ID" | python3 -c "
import json,sys
d=json.load(sys.stdin); m=d['metadata']
print(f\"  state    : {d.get('state')}  submitted={d.get('submitted')}\")
print(f\"  version  : {m.get('version')}   licence: {m.get('license')}\")
for f in d.get('files',[]): print(f\"  file     : {f['filename']}  {f['checksum']}\")
print('  scope line in description:', 'No model checkpoint is recommended for release' in m.get('description',''))"

echo
echo "Staged, NOT published. Review the draft in the Zenodo UI, then publish there by hand."
echo "https://zenodo.org/uploads/$DEP_ID"
