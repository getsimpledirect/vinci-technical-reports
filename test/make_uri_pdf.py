#!/usr/bin/env python3
"""One-page PDF whose ONLY notable property is the set of /URI link targets it
carries, so the PDF_FORBID_URI gate in assemble_release.sh can be exercised
without a TeX toolchain and without depending on a real report PDF.

    make_uri_pdf.py out.pdf <uri> [<uri> ...]

Each URI becomes a real /Link annotation with a /URI action (not a text
mention), which is exactly what scripts/pdf_uris.py extracts and what pdftotext
cannot see. The page text is the one string the fixture release.conf REQUIREs
so every text gate ahead of the URI gate passes and the URI gate is reached.

The fixture uses the base-14 Helvetica, which is not embedded; the font gate
that runs AFTER the URI gate therefore fails on this fixture. That is expected:
the test reads the URI gate's own messages, not the script's exit status, and
uses real report PDFs for the end-to-end case.
"""
import pathlib
import sys


def pdf_string(value: str) -> str:
    return "(" + value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)") + ")"


def build(uris: list[str]) -> bytes:
    content = (
        "BT /F1 14 Tf 40 740 Td 18 TL\n"
        "(Runtime Pass Is Not Correctness) Tj T*\n"
        "(URI-gate fixture) Tj T*\n"
        "ET"
    )
    annots = [f"{6 + index} 0 R" for index in range(len(uris))]
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R "
        f"/Annots [{' '.join(annots)}] >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
    ]
    for index, uri in enumerate(uris):
        top = 700 - 20 * index
        objs.append(
            f"<< /Type /Annot /Subtype /Link /Rect [40 {top - 14} 400 {top}] /Border [0 0 0] "
            f"/A << /Type /Action /S /URI /URI {pdf_string(uri)} >> >>"
        )
    out, offsets = "%PDF-1.4\n", []
    for number, obj in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{number} 0 obj\n{obj}\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n"
    for offset in offsets:
        out += f"{offset:010d} 00000 n \n"
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
    return out.encode("latin-1")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: make_uri_pdf.py out.pdf <uri> [<uri> ...]")
    pathlib.Path(sys.argv[1]).write_bytes(build(sys.argv[2:]))
