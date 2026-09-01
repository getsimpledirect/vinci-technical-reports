from pathlib import Path

root = Path(__file__).resolve().parents[1]
src = (root / 'report' / 'Vinci_Technical_Report_No_2.md').read_text(encoding='utf-8')
# Strip YAML frontmatter.
if src.startswith('---\n'):
    end = src.find('\n---\n', 4)
    src = src[end + 5:]
# Replace the Markdown title block with a semantic publication hero.
start = src.index('# Character Transfer Across Three Model Families')
abstract = src.index('## Abstract')
hero = '''<header class="report-hero">
  <p class="eyebrow">Vinci Technical Report No. 2 <span>September 2026</span></p>
  <h1>Character Transfer Across Three Model Families</h1>
  <p class="subtitle">Reduced unsupported assertions, impaired grounded answering, and a failed utility-preservation bar</p>
  <p class="authors"><strong>George Pu</strong> and <strong>Ayush Naik</strong></p>
  <p class="affiliation">SimpleDirect / Vinci Research, Toronto, Canada</p>
  <div class="status-grid" role="note" aria-label="Publication status" markdown="0">
<span>Version 1.0</span>
<span>Development-tier evidence</span>
<span>Internal review only</span>
<span>External peer review not performed</span>
  </div>
</header>

'''
src = hero + src[abstract:]
(root / 'source' / 'Vinci_Technical_Report_No_2_html.md').write_text(src, encoding='utf-8')
