#!/usr/bin/env python3
"""Print every URI a PDF links to, one per line.

pdftotext cannot see these: a hyperlink's target lives in a /URI annotation,
while only its visible label reaches the extracted text. TR3's report linked a
private repository behind the visible label "getsimpledirect/vinci-gpu-research",
so a text-level FORBID on the URL matched nothing and the gate was inert.
Annotations in modern pandoc/xelatex output sit inside compressed object
streams, so both the raw bytes and the inflated streams are scanned.
"""
import re, sys, zlib

PAT = re.compile(rb"/URI\s*\(([^)]{4,600})\)")

def uris(path):
    data = open(path, "rb").read()
    found = set(PAT.findall(data))
    for m in re.finditer(rb"stream\r?\n", data):
        chunk = data[m.end():m.end() + 2_000_000]
        try:
            found.update(PAT.findall(zlib.decompressobj().decompress(chunk)))
        except zlib.error:
            pass
    return sorted(u.decode("latin1") for u in found)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: pdf_uris.py <file.pdf>")
    for u in uris(sys.argv[1]):
        print(u)
