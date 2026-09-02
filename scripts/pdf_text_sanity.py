#!/usr/bin/env python3
"""Fail when a PDF's extracted text contains private-use code points.

Report No. 3's redesign set Inter as the sans face. Inter's contextual
alternates swap in case-sensitive forms of hyphen and plus next to capitals and
digits, and in the subsetted font those alternates carry Private Use Area code
points in the ToUnicode map. The glyphs LOOK right on the page; only extraction
is wrong. "Qwen3.8-27B" came out "Qwen3.827B", "P-BREVE-01" came out
"PBREVE01", and -- worst -- the signed headline metrics "-10.9% / +4.9%" lost
their signs entirely.

That is not cosmetic. Extracted text is what indexers, screen readers,
citation managers and anyone copying a number actually receive, so a sign that
vanishes there is a wrong number in every downstream surface.

Any private-use code point in an archival PDF is a defect: by definition it has
no agreed meaning outside the font that emitted it.
"""
import subprocess, sys, unicodedata
from collections import Counter, defaultdict

def private_use(cp):
    return 0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0xFFFFD or 0x100000 <= cp <= 0x10FFFD

def main(path):
    try:
        text = subprocess.run(["pdftotext", path, "-"],
                              capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        print(f"FAIL cannot extract text from {path}: {e}", file=sys.stderr)
        return 2
    counts, where = Counter(), defaultdict(list)
    for lineno, line in enumerate(text.splitlines(), 1):
        for ch in line:
            if private_use(ord(ch)):
                counts[ch] += 1
                if len(where[ch]) < 5:
                    where[ch].append((lineno, line.strip()[:90]))
    if not counts:
        print(f"ok  no private-use code points ({len(text)} chars scanned)")
        return 0
    total = sum(counts.values())
    print(f"FAIL {total} private-use code point(s), {len(counts)} distinct", file=sys.stderr)
    for ch, n in counts.most_common():
        print(f"  U+{ord(ch):04X} x{n}", file=sys.stderr)
        for lineno, ctx in where[ch]:
            print(f"      line {lineno}: {ctx}", file=sys.stderr)
    return 1

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pdf_text_sanity.py <file.pdf>")
    sys.exit(main(sys.argv[1]))
