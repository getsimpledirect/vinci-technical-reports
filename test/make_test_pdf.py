#!/usr/bin/env python3
"""Minimal PDF carrying the strings zenodo_stage.sh gates on, so the guards can
be exercised without a TeX toolchain."""
import pathlib, sys
def mkpdf(path, lines):
    content = "BT /F1 12 Tf 40 750 Td 14 TL\n" + "".join(f"({l}) Tj T*\n" for l in lines) + "ET"
    objs = ["<< /Type /Catalog /Pages 2 0 R >>",
            "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
            "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
            f"<< /Length {len(content)} >>\nstream\n{content}\nendstream"]
    out, offs = "%PDF-1.4\n", []
    for i, o in enumerate(objs, 1):
        offs.append(len(out)); out += f"{i} 0 obj\n{o}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n"
    for off in offs: out += f"{off:010d} 00000 n \n"
    out += f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    pathlib.Path(path).write_bytes(out.encode('latin-1'))
# Bullet, matching what vinci_tr2_template.tex actually prints — a hyphen here
# would let a gate pass in tests that fails on the real PDF.
# \225 is bullet under WinAnsiEncoding — the separator the real template prints.
# A hyphen here would let the gate pass in tests and fail on the real PDF.
sep = sys.argv[2] if len(sys.argv) > 2 else "\\225"
mkpdf(sys.argv[1], [f"Version 1.0 {sep} 1 September 2026", "Outstanding Evidence Work"])
