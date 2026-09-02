#!/usr/bin/env python3
"""Minimal PDF whose ToUnicode map sends a glyph to a private-use code point.

This reproduces the Report No. 3 redesign defect without a TeX toolchain: Inter
maps hyphen.case.tf / plus.case.tf into the PUA, XeLaTeX derives ToUnicode from
the font cmap, and the page renders correctly while extraction yields U+EE55.

  make_pua_pdf.py out.pdf         -> text extracts as "A-B", clean (control)
  make_pua_pdf.py out.pdf --pua   -> the hyphen extracts as U+EE55 (defective)
"""
import pathlib, sys

def mkpdf(path, pua):
    # 'A' 'hyphen' 'B' by byte; only the ToUnicode mapping differs.
    content = "BT /F1 24 Tf 40 700 Td (A-B signed 10.9) Tj ET"
    hyphen_target = "EE55" if pua else "002D"
    cmap = (
        "/CIDInit /ProcSet findresource begin 12 dict begin begincmap\n"
        "/CMapName /Custom def /CMapType 2 def\n"
        "1 begincodespacerange <00> <FF> endcodespacerange\n"
        f"1 beginbfchar <2D> <{hyphen_target}> endbfchar\n"
        "endcmap CMapName currentdict /CMap defineresource pop end end"
    )
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica "
        "/Encoding /WinAnsiEncoding /ToUnicode 6 0 R >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
        f"<< /Length {len(cmap)} >>\nstream\n{cmap}\nendstream",
    ]
    out, offs = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out)); out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n"
    for off in offs: out += f"{off:010d} 00000 n \n"
    out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    pathlib.Path(path).write_bytes(out.encode("latin-1"))

if __name__ == "__main__":
    mkpdf(sys.argv[1], "--pua" in sys.argv)
