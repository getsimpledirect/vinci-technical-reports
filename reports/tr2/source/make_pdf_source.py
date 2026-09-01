from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
src = (root/'report'/'Vinci_Technical_Report_No_2.md').read_text(encoding='utf-8')
# Keep body from section 1 onward.
body = src[src.index('## 1. Introduction'):]

# Replace figures with raw LaTeX includes.
fig_map = {
    '![Unsupported assertion rates for C0 and C3. UAR declined under both judges in all three families.](../figures/figure2_uar_by_family_and_judge.png)': r'\input{figure2.tex}',
    '![Refusal-adjusted UAR-ACC frontier under Judge B. The pre-registered success region required at least 5 points of UAR improvement and no more than 3 points of ACC loss.](../figures/figure3_refusal_adjusted_frontier.png)': r'\input{figure3.tex}',
    '![G1 reliability estimates across the void and canonical executions. The void run is not a competing gate result, but it exposes repeatability risk.](../figures/figure4_g1_judge_repeatability.png)': r'\input{figure4.tex}',
    '![Summary of the release claim boundary.](../figures/figure5_result_summary.png)': r'\input{figure5.tex}',
}
for k,v in fig_map.items(): body=body.replace(k,v)

# Long hexadecimal identifiers are evidence, but Markdown code spans become
# unbreakable texttt boxes in LaTeX and can overprint the adjacent column.
# seqsplit keeps every byte visible while allowing safe line breaks.
body = re.sub(
    r'`([0-9a-f]{48,})`',
    lambda m: r'\texttt{\seqsplit{' + m.group(1) + '}}',
    body,
)

# Replace known Markdown tables with raw TeX input by their first header line.
tables = [
    ('| Family | Frozen base | Revision | Purpose |', r'\input{table_model_panel.tex}'),
    ('| Component | Frozen value |', r'\input{table_intervention.tex}'),
    ('| Family | Judge A: C0 to C3 | Judge A improvement | Judge B: C0 to C3 | Judge B improvement | Judge spread |', r'\input{table_uar.tex}'),
    ('| Family | Raw UAR gain | Adjusted UAR gain | Gain surviving | Raw ACC change | Adjusted ACC change | ACC loss per adjusted UAR gain |', r'\input{table_adjusted.tex}'),
    ('| Outcome | Effective n | AC1 | 95% cluster-bootstrap interval | Raw agreement | Gate |', r'\input{table_reliability.tex}'),
    ('| Claim | Status | Evidence | Permitted public wording |', r'\input{table_claims.tex}'),
    ('| Field | Value |', r'\input{table_provenance.tex}'),
    ('| Planned element | Actual disposition | Consequence |', r'\input{table_deviations.tex}'),
]
lines = body.splitlines()
out=[]
i=0
while i < len(lines):
    line=lines[i]
    match=next(((sig,repl) for sig,repl in tables if line.strip()==sig),None)
    if match:
        # Drop prior blank only if duplicate spacing is excessive.
        out.append(match[1])
        i += 1
        # Skip separator and rows until blank.
        while i < len(lines) and lines[i].strip(): i += 1
        continue
    stripped = line.strip()

    # The manuscript carries explicit section numbers for plain-Markdown reading,
    # while LaTeX numbers headings itself. Remove the textual prefixes so the PDF
    # never renders "1 1. Introduction" or "2.1 2.1 ...".
    if stripped.startswith('#'):
        m = re.match(r'^(#{2,6})\s+(.*)$', line)
        if m:
            hashes, title = m.groups()
            title = re.sub(r'^\d+(?:\.\d+)*\.?(?:\s+)', '', title)
            line = f'{hashes} {title}'
            stripped = line.strip()

    # Back matter headings are intentionally unnumbered, matching Report No. 1.
    if stripped == '## Author Contributions':
        out.append(r'\section*{Author Contributions}')
    elif stripped == '## Competing Interests, Funding, and AI Assistance':
        out.append(r'\section*{Competing Interests, Funding, and AI Assistance}')
    elif stripped == '## References':
        out.append(r'\section*{References}')
    elif stripped == '## Appendix A. Claim-to-Evidence Boundary':
        out.append(r'\clearpage')
        out.append(r'\onecolumn')
        out.append(r'\appendix')
        out.append('## Claim-to-Evidence Boundary')
    elif stripped == '## Appendix B. Key Provenance Values':
        out.append('## Key Provenance Values')
    elif stripped == '## Appendix C. Material Deviations and Unfinished Charter Items':
        out.append('## Material Deviations and Unfinished Charter Items')
    elif stripped == '## Appendix D. Outstanding Evidence Work':
        out.append('## Outstanding Evidence Work')
    else:
        out.append(line)
    i += 1

pdf_md='\n'.join(out)+'\n'
(root/'source'/'latex'/'Vinci_Technical_Report_No_2_pdf.md').write_text(pdf_md,encoding='utf-8')
