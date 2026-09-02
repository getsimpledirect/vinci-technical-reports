#!/usr/bin/env python3
"""Build and verify TR3 derivatives without mutating its historical v1.0 PDF.

The sole editable manuscript is source/report_body.md. Everything this script
writes is derived from it or from committed frozen figures. It has no network,
upload, tag, release, publication, or PDF-replacement operation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
import xml.etree.ElementTree as ET


PACKAGE = Path(__file__).resolve().parents[1]
SOURCE = PACKAGE / "source" / "report_body.md"
REPORT = PACKAGE / "report"
ARXIV = PACKAGE / "arxiv"
CONTRACT = PACKAGE / "release" / "SEMANTIC_CONTRACT.json"
FIXED_ZIP_TIME = (2026, 9, 1, 0, 0, 0)
PANDOC_VERSION = "3.10"
LATEX_TABLE_LAYOUTS = [
    "p{0.48\\linewidth}p{0.23\\linewidth}p{0.23\\linewidth}",
    "p{0.48\\linewidth}p{0.18\\linewidth}p{0.28\\linewidth}",
    "p{0.72\\linewidth}p{0.22\\linewidth}",
    "p{0.34\\linewidth}p{0.28\\linewidth}p{0.32\\linewidth}",
    "p{0.34\\linewidth}p{0.20\\linewidth}p{0.20\\linewidth}p{0.20\\linewidth}",
    "p{0.48\\linewidth}p{0.23\\linewidth}p{0.23\\linewidth}",
    "p{0.34\\linewidth}p{0.20\\linewidth}p{0.20\\linewidth}p{0.20\\linewidth}",
    "p{0.48\\linewidth}p{0.30\\linewidth}p{0.16\\linewidth}",
    "p{0.48\\linewidth}p{0.23\\linewidth}p{0.23\\linewidth}",
    "p{0.48\\linewidth}p{0.23\\linewidth}p{0.23\\linewidth}",
    "p{0.48\\linewidth}p{0.18\\linewidth}p{0.28\\linewidth}",
    "p{0.48\\linewidth}p{0.46\\linewidth}",
    "p{0.34\\linewidth}p{0.28\\linewidth}p{0.32\\linewidth}",
    "p{0.34\\linewidth}p{0.28\\linewidth}p{0.32\\linewidth}",
    "p{0.28\\linewidth}p{0.25\\linewidth}p{0.21\\linewidth}p{0.20\\linewidth}",
    "p{0.28\\linewidth}p{0.25\\linewidth}p{0.21\\linewidth}p{0.20\\linewidth}",
    "p{0.34\\linewidth}p{0.28\\linewidth}p{0.32\\linewidth}",
    "p{0.28\\linewidth}p{0.25\\linewidth}p{0.21\\linewidth}p{0.20\\linewidth}",
]
LATEX_BREAKABLE_LITERALS = [
    "pbr2.g4.full-recipe-insufficient.015",
    "p-breve-01-r2/docs/BLIND-ADVERSARIAL-POPULATION.md",
]


class GateFailure(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(args: list[str], *, cwd: Path | None = None) -> str:
    proc = subprocess.run(
        args,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "SOURCE_DATE_EPOCH": "1788220800"},
    )
    if proc.returncode:
        raise GateFailure(
            f"command failed ({proc.returncode}): {' '.join(args)}\n{proc.stderr[-2000:]}"
        )
    if "Could not fetch resource" in proc.stderr:
        raise GateFailure(f"renderer omitted a resource:\n{proc.stderr[-2000:]}")
    return proc.stdout


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"\A---\n(.*?)\n---\n+", text, re.S)
    if not match:
        raise GateFailure("canonical manuscript has no YAML front matter")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip()] = value.strip().strip('"')
    required = {"title", "subtitle", "author", "date"}
    if set(meta) != required:
        raise GateFailure(f"front matter keys are {sorted(meta)}, expected {sorted(required)}")
    return meta, text[match.end() :]


def normalized(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).casefold()
    text = text.replace("−", "-")
    return " ".join(re.findall(r"[a-z0-9]+(?:[.+%-][a-z0-9]+)*", text))


def assert_contract_text(name: str, text: str, contract: dict, *, require_all: bool) -> None:
    value = normalized(text)
    for marker in contract["forbidden_on_any_report_or_source_surface"]:
        if normalized(marker) in value:
            raise GateFailure(f"{name}: forbidden pre-publication marker: {marker}")
    if require_all:
        for phrase in contract["required_on_every_report_surface"]:
            if normalized(phrase) not in value:
                raise GateFailure(f"{name}: missing semantic-contract phrase: {phrase}")


def verify_historical_pdf(path: Path, contract: dict) -> None:
    """Verify the frozen artifact and its disclosed divergence; do not certify it."""
    if sha256(path) != os.environ["HISTORICAL_PDF_SHA256"]:
        raise GateFailure("historical v1.0 PDF bytes changed")
    info = run(["pdfinfo", str(path)])
    pages = re.search(r"^Pages:\s+(\d+)$", info, re.M)
    if not pages or int(pages.group(1)) != contract["historical_v1_pdf_pages"]:
        raise GateFailure("historical v1.0 PDF page count differs from its frozen record")
    text = normalized(extract_surface("pdf", path))
    for defect in contract["known_historical_v1_pdf_divergence"]:
        if normalized(defect["marker"]) not in text:
            raise GateFailure(
                "historical v1.0 PDF no longer exhibits its disclosed divergence: "
                f"page {defect['page']} / {defect['marker']}"
            )


def deterministic_zip(source: Path, target: Path, *, prefix: str = "") -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(p for p in source.rglob("*") if p.is_file() and not is_transient(p)):
            relative = path.relative_to(source).as_posix()
            name = f"{prefix.rstrip('/')}/{relative}" if prefix else relative
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def is_transient(path: Path) -> bool:
    return "__pycache__" in path.parts or path.name == ".DS_Store" or path.suffix == ".pyc"


def canonicalize_docx(path: Path) -> None:
    staging = path.with_suffix(".normalized.docx")
    with zipfile.ZipFile(path) as source, zipfile.ZipFile(
        staging, "w", zipfile.ZIP_DEFLATED, compresslevel=9
    ) as target:
        for name in sorted(source.namelist()):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            target.writestr(info, source.read(name), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    staging.replace(path)


def render(destination: Path, arxiv_zip_name: str) -> dict[str, Path]:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise GateFailure("pandoc is required")
    version = run([pandoc, "--version"]).splitlines()[0].split()[-1]
    if version != PANDOC_VERSION:
        raise GateFailure(f"pandoc {PANDOC_VERSION} is required for deterministic derivatives; found {version}")

    text = SOURCE.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    out_report = destination / "report"
    out_arxiv = destination / "arxiv" / "source"
    out_report.mkdir(parents=True)
    out_arxiv.mkdir(parents=True)

    md = out_report / "Vinci_Technical_Report_No_3.md"
    html = out_report / "Vinci_Technical_Report_No_3.html"
    docx = out_report / "Vinci_Technical_Report_No_3.docx"
    md.write_text(text, encoding="utf-8")

    run(
        [
            pandoc,
            "report_body.md",
            "--from=gfm+yaml_metadata_block",
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--css=report.css",
            "--embed-resources",
            "--resource-path=..",
            f"--output={html}",
        ],
        cwd=PACKAGE / "source",
    )
    run(
        [
            pandoc,
            "report_body.md",
            "--from=gfm+yaml_metadata_block",
            "--reference-doc=reference.docx",
            "--resource-path=..",
            "--toc",
            "--toc-depth=3",
            f"--output={docx}",
        ],
        cwd=PACKAGE / "source",
    )
    canonicalize_docx(docx)

    arxiv_body = text.replace("](../figures/", "](figures/")
    (out_arxiv / "body.md").write_text(arxiv_body, encoding="utf-8")
    (out_arxiv / "README.md").write_text(
        "# arXiv source\n\n"
        "Generated from `source/report_body.md`. Compile with two XeLaTeX passes:\n\n"
        "```sh\n"
        "xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex\n"
        "xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex\n"
        "```\n\n"
        "The archive is self-contained and requires no shell escape or external downloads.\n",
        encoding="utf-8",
    )
    (out_arxiv / "00README.json").write_text(
        json.dumps({"process": {"compiler": "xelatex"}}, indent=2) + "\n",
        encoding="utf-8",
    )
    figure_dir = out_arxiv / "figures"
    figure_dir.mkdir()
    for index in range(1, 7):
        stem = next((PACKAGE / "figures").glob(f"figure{index}_*.png"), None)
        if stem is None:
            raise GateFailure(f"missing frozen figure {index} PNG")
        shutil.copy2(stem, figure_dir / stem.name)

    run(
        [
            pandoc,
            "body.md",
            "--from=gfm",
            "--standalone",
            "--toc",
            "--toc-depth=3",
            "--pdf-engine=xelatex",
            "-V",
            "geometry:margin=0.78in",
            "-M",
            f"title={meta['title']}",
            "-M",
            f"subtitle={meta['subtitle']}",
            "-M",
            f"author={meta['author']}",
            "-M",
            f"date={meta['date']}",
            "--resource-path=.",
            "--output=main.tex",
        ],
        cwd=out_arxiv,
    )
    tex_path = out_arxiv / "main.tex"
    tex = tex_path.read_text(encoding="utf-8")
    seen = 0
    def replace_layout(match: re.Match[str]) -> str:
        nonlocal seen
        if seen >= len(LATEX_TABLE_LAYOUTS):
            raise GateFailure("generated TeX contains more tables than the layout authority")
        layout = LATEX_TABLE_LAYOUTS[seen]
        seen += 1
        return rf"\begin{{longtable}}[]{{@{{}}{layout}@{{}}}}"
    tex = re.sub(r"\\begin\{longtable\}\[\]\{@\{\}[^\n]*@\{\}\}", replace_layout, tex)
    if seen != len(LATEX_TABLE_LAYOUTS):
        raise GateFailure(f"generated TeX contains {seen} tables, expected {len(LATEX_TABLE_LAYOUTS)}")
    for literal in LATEX_BREAKABLE_LITERALS:
        old = rf"\texttt{{{literal}}}"
        if old not in tex:
            raise GateFailure(f"expected long TeX literal is missing: {literal}")
        tex = tex.replace(old, rf"\path{{{literal}}}")
    tex_path.write_text(tex, encoding="utf-8")
    archive = destination / "arxiv" / arxiv_zip_name
    deterministic_zip(out_arxiv, archive)
    return {"md": md, "html": html, "docx": docx, "arxiv_zip": archive, "arxiv": out_arxiv}


def extract_surface(kind: str, path: Path) -> str:
    if kind == "pdf":
        return run(["pdftotext", str(path), "-"])
    if kind == "docx":
        with zipfile.ZipFile(path) as archive:
            root = ET.fromstring(archive.read("word/document.xml"))
        return " ".join(node.text or "" for node in root.iter() if node.tag.endswith("}t"))
    return run(["pandoc", str(path), f"--from={kind}", "--to=plain"])


def verify_semantics(paths: dict[str, Path], contract: dict) -> None:
    assert_contract_text("canonical Markdown", SOURCE.read_text(encoding="utf-8"), contract, require_all=True)
    assert_contract_text("generated Markdown", paths["md"].read_text(encoding="utf-8"), contract, require_all=True)
    assert_contract_text("generated HTML", extract_surface("html", paths["html"]), contract, require_all=True)
    assert_contract_text("generated DOCX", extract_surface("docx", paths["docx"]), contract, require_all=True)
    assert_contract_text("arXiv Markdown", (paths["arxiv"] / "body.md").read_text(), contract, require_all=True)
    assert_contract_text("arXiv TeX", (paths["arxiv"] / "main.tex").read_text(), contract, require_all=False)

    with zipfile.ZipFile(paths["docx"]) as archive:
        media = [name for name in archive.namelist() if name.startswith("word/media/")]
    if len(media) != contract["figure_count"]:
        raise GateFailure(f"DOCX embeds {len(media)} figures, expected {contract['figure_count']}")
    html = paths["html"].read_text(encoding="utf-8")
    if html.count("data:image/png;base64,") < contract["figure_count"]:
        raise GateFailure("HTML does not embed all six report figures")


def verify_arxiv_compile(paths: dict[str, Path], contract: dict) -> tuple[int, Path]:
    source = paths["arxiv"]
    xelatex = shutil.which("xelatex")
    tectonic = shutil.which("tectonic")
    if xelatex:
        command = [xelatex, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
        run(command, cwd=source)
        run(command, cwd=source)
    elif tectonic:
        run([tectonic, "main.tex"], cwd=source)
    else:
        raise GateFailure("XeLaTeX or Tectonic is required to prove the arXiv source compiles")
    pdf = source / "main.pdf"
    assert_contract_text("compiled arXiv PDF", extract_surface("pdf", pdf), contract, require_all=True)
    info = run(["pdfinfo", str(pdf)])
    pages = re.search(r"^Pages:\s+(\d+)$", info, re.M)
    if not pages or int(pages.group(1)) < 30:
        raise GateFailure("compiled arXiv PDF is unexpectedly short")
    bbox = source / "main.bbox.xml"
    run(["pdftotext", "-bbox-layout", str(pdf), str(bbox)])
    root = ET.parse(bbox).getroot()
    ns = {"x": "http://www.w3.org/1999/xhtml"}
    outside: list[str] = []
    for page_number, page in enumerate(root.findall(".//x:page", ns), 1):
        width = float(page.attrib["width"])
        for word in page.findall(".//x:word", ns):
            if float(word.attrib["xMin"]) < 1 or float(word.attrib["xMax"]) > width - 1:
                outside.append(f"page {page_number}: {word.text!r}")
    if outside:
        raise GateFailure(f"compiled arXiv PDF has text outside the page: {outside[:5]}")
    return int(pages.group(1)), pdf


def compare_file(expected: Path, actual: Path, label: str) -> None:
    if not actual.is_file():
        raise GateFailure(f"missing generated artifact: {actual.relative_to(PACKAGE)}")
    if expected.read_bytes() != actual.read_bytes():
        raise GateFailure(f"stale generated artifact: {label}; run source/rebuild_all.sh --write")


def expected_receipt(arxiv_pages: int) -> dict:
    artifacts = {
        "canonical_markdown": PACKAGE / "source" / "report_body.md",
        "generated_markdown": REPORT / "Vinci_Technical_Report_No_3.md",
        "html": REPORT / "Vinci_Technical_Report_No_3.html",
        "docx": REPORT / "Vinci_Technical_Report_No_3.docx",
        "historical_v1_pdf": REPORT / os.environ["HISTORICAL_PDF_NAME"],
        "unpublished_candidate_pdf": REPORT / os.environ["CANDIDATE_PDF_NAME"],
        "arxiv_markdown": ARXIV / "source" / "body.md",
        "arxiv_tex": ARXIV / "source" / "main.tex",
        "arxiv_source_zip": ARXIV / os.environ["ARXIV_ZIP_NAME"],
    }
    return {
        "schema_version": 1,
        "report_version": os.environ["REPORT_VERSION"],
        "package_revision": os.environ["PACKAGE_REVISION"],
        "publication_status": "Version 1.0 is already published and immutable; this repository-forward repair is not published",
        "source_authority": "source/report_body.md",
        "renderer": f"pandoc {PANDOC_VERSION}",
        "qa": {
            "semantic_contract": "passed across corrected Markdown, HTML, DOCX, arXiv Markdown, TeX, and unpublished candidate PDF",
            "historical_v1_pdf_pages": 43,
            "historical_v1_pdf_preserved": True,
            "historical_v1_pdf_semantic_status": "known divergent; retained only as immutable publication evidence",
            "docx_embedded_figures": 6,
            "html_embedded_figures": 6,
            "arxiv_compile_pages": arxiv_pages,
            "arxiv_words_outside_page": 0,
        },
        "artifact_sha256": {name: sha256(path) for name, path in artifacts.items()},
        "remaining_publication_decision": "Optional arXiv submission and any new GitHub/Zenodo version require separate authority",
    }


def write_inventory(report_version: str, package_revision: str, package_name: str) -> None:
    manifest = PACKAGE / "MANIFEST.json"
    checksums = PACKAGE / "CHECKSUMS.sha256"
    excluded = {manifest.name, checksums.name}
    files = [p for p in PACKAGE.rglob("*") if p.is_file() and p.name not in excluded and not is_transient(p)]
    entries = [
        {
            "path": path.relative_to(PACKAGE).as_posix(),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(files)
    ]
    data = {
        "schema_version": 1,
        "report_version": report_version,
        "package_revision": package_revision,
        "package": package_name,
        "publication_record": "10.5281/zenodo.22241477",
        "publication_source_commit": "128dea8b4013cdb3398c98edab5dc930e24c51d2",
        "source_authority": "source/report_body.md",
        "historical_pdf_sha256": os.environ["HISTORICAL_PDF_SHA256"],
        "inventory_excludes": sorted(excluded),
        "file_count": len(entries),
        "files": entries,
    }
    manifest.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checksum_paths = sorted(p for p in PACKAGE.rglob("*") if p.is_file() and p != checksums and not is_transient(p))
    checksums.write_text(
        "".join(f"{sha256(path)}  {path.relative_to(PACKAGE).as_posix()}\n" for path in checksum_paths),
        encoding="utf-8",
    )


def parse_manifest(data: object, expected_meta: dict[str, object]) -> dict[str, dict]:
    if not isinstance(data, dict):
        raise GateFailure("manifest root must be an object")
    required = {
        "schema_version",
        "report_version",
        "package_revision",
        "package",
        "publication_record",
        "publication_source_commit",
        "source_authority",
        "historical_pdf_sha256",
        "inventory_excludes",
        "file_count",
        "files",
    }
    missing = sorted(required - set(data))
    if missing:
        raise GateFailure(f"manifest missing required field(s): {missing}")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise GateFailure("manifest schema_version must be integer 1")
    excludes = data["inventory_excludes"]
    if not isinstance(excludes, list) or any(not isinstance(value, str) for value in excludes):
        raise GateFailure("manifest inventory_excludes must be a list of strings")
    if excludes != sorted(set(excludes)) or excludes != ["CHECKSUMS.sha256", "MANIFEST.json"]:
        raise GateFailure("manifest inventory_excludes must name the two inventories exactly once")
    if type(data["file_count"]) is not int or data["file_count"] < 0:
        raise GateFailure("manifest file_count must be a non-negative integer")
    if not isinstance(data["files"], list):
        raise GateFailure("manifest files must be a list")
    for key, value in expected_meta.items():
        if data[key] != value:
            raise GateFailure(f"manifest {key}={data[key]!r}, expected {value!r}")
    listed: dict[str, dict] = {}
    digest_re = re.compile(r"[0-9a-f]{64}\Z")
    for index, entry in enumerate(data["files"]):
        if not isinstance(entry, dict):
            raise GateFailure(f"manifest file entry {index} must be an object")
        if set(entry) != {"path", "size_bytes", "sha256"}:
            raise GateFailure(f"manifest file entry {index} has invalid fields")
        name = entry["path"]
        if not isinstance(name, str) or not name or name.startswith("/") or ".." in Path(name).parts:
            raise GateFailure(f"manifest file entry {index} has an invalid path")
        if name in listed:
            raise GateFailure(f"duplicate manifest path: {name}")
        if type(entry["size_bytes"]) is not int or entry["size_bytes"] < 0:
            raise GateFailure(f"manifest file entry {name} has invalid size_bytes")
        if not isinstance(entry["sha256"], str) or not digest_re.fullmatch(entry["sha256"]):
            raise GateFailure(f"manifest file entry {name} has invalid sha256")
        listed[name] = entry
    return listed


def parse_checksums(text: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    row_re = re.compile(r"([0-9a-f]{64})  (\S(?:.*\S)?)\Z")
    for index, line in enumerate(text.splitlines(), 1):
        match = row_re.fullmatch(line)
        if not match:
            raise GateFailure(f"malformed checksum row {index}")
        digest, name = match.groups()
        if name in rows:
            raise GateFailure(f"duplicate checksum path: {name}")
        rows[name] = digest
    return rows


def verify_inventory(
    report_version: str,
    package_revision: str,
    package_name: str,
    *,
    package: Path = PACKAGE,
) -> None:
    manifest_path = package / "MANIFEST.json"
    checksum_path = package / "CHECKSUMS.sha256"
    transient = [p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file() and is_transient(p)]
    if transient:
        raise GateFailure(f"transient files must not enter a release package: {transient}")
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_meta: dict[str, object] = {
        "schema_version": 1,
        "report_version": report_version,
        "package_revision": package_revision,
        "package": package_name,
        "publication_record": "10.5281/zenodo.22241477",
        "publication_source_commit": "128dea8b4013cdb3398c98edab5dc930e24c51d2",
        "source_authority": "source/report_body.md",
        "historical_pdf_sha256": os.environ["HISTORICAL_PDF_SHA256"],
        "inventory_excludes": ["CHECKSUMS.sha256", "MANIFEST.json"],
    }
    listed = parse_manifest(data, expected_meta)
    actual = {
        p.relative_to(package).as_posix(): p
        for p in package.rglob("*")
        if p.is_file() and p.name not in {manifest_path.name, checksum_path.name} and not is_transient(p)
    }
    if set(listed) != set(actual) or data.get("file_count") != len(actual):
        raise GateFailure(
            f"manifest coverage mismatch: missing={sorted(set(actual)-set(listed))}, "
            f"phantom={sorted(set(listed)-set(actual))}, count={data.get('file_count')}/{len(actual)}"
        )
    for name, path in actual.items():
        entry = listed[name]
        if entry["size_bytes"] != path.stat().st_size or entry["sha256"] != sha256(path):
            raise GateFailure(f"manifest digest mismatch: {name}")
    checksum_lines = parse_checksums(checksum_path.read_text(encoding="utf-8"))
    expected_checksums = {
        p.relative_to(package).as_posix(): sha256(p)
        for p in package.rglob("*")
        if p.is_file() and p != checksum_path and not is_transient(p)
    }
    if checksum_lines != expected_checksums:
        raise GateFailure("checksum inventory does not exactly cover the package plus manifest")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["check", "write"])
    args = parser.parse_args()
    required_env = [
        "REPORT_VERSION",
        "PACKAGE_REVISION",
        "PACKAGE_DIR_NAME",
        "ARXIV_ZIP_NAME",
        "HISTORICAL_PDF_SHA256",
        "HISTORICAL_PDF_NAME",
        "CANDIDATE_PDF_NAME",
        "ZIP_BASE",
    ]
    missing = [name for name in required_env if not os.environ.get(name)]
    if missing:
        raise GateFailure(f"release.conf did not provide: {', '.join(missing)}")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    historical_pdf = REPORT / os.environ["HISTORICAL_PDF_NAME"]
    verify_historical_pdf(historical_pdf, contract)

    with tempfile.TemporaryDirectory(prefix="tr3-build.") as temp_name:
        temp = Path(temp_name)
        built = render(temp, os.environ["ARXIV_ZIP_NAME"])
        verify_semantics(built, contract)
        arxiv_pages, compiled_pdf = verify_arxiv_compile(built, contract)
        built["candidate_pdf"] = compiled_pdf

        generated = {
            built["md"]: REPORT / built["md"].name,
            built["html"]: REPORT / built["html"].name,
            built["docx"]: REPORT / built["docx"].name,
            built["candidate_pdf"]: REPORT / os.environ["CANDIDATE_PDF_NAME"],
            built["arxiv"] / "body.md": ARXIV / "source" / "body.md",
            built["arxiv"] / "main.tex": ARXIV / "source" / "main.tex",
            built["arxiv"] / "README.md": ARXIV / "source" / "README.md",
            built["arxiv"] / "00README.json": ARXIV / "source" / "00README.json",
            built["arxiv_zip"]: ARXIV / os.environ["ARXIV_ZIP_NAME"],
        }
        if args.mode == "write":
            for source, target in generated.items():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            for old in [
                ARXIV / "Vinci_TR3_arXiv_v1.0.1_source.zip",
                ARXIV / "Vinci_TR3_arXiv_v1.0.3_source.zip",
                PACKAGE / "source" / "tr3_fixed.tex",
            ]:
                if old.exists():
                    old.unlink()
            receipt = PACKAGE / "release" / "Vinci_TR3_PACKAGE_RECEIPT_v1.0.3.json"
            receipt.write_text(json.dumps(expected_receipt(arxiv_pages), indent=2) + "\n", encoding="utf-8")
            write_inventory(
                os.environ["REPORT_VERSION"],
                os.environ["PACKAGE_REVISION"],
                os.environ["PACKAGE_DIR_NAME"],
            )
        else:
            for source, target in generated.items():
                compare_file(source, target, target.relative_to(PACKAGE).as_posix())
            for obsolete in [
                ARXIV / "Vinci_TR3_arXiv_v1.0.1_source.zip",
                ARXIV / "Vinci_TR3_arXiv_v1.0.3_source.zip",
                PACKAGE / "source" / "tr3_fixed.tex",
            ]:
                if obsolete.exists():
                    raise GateFailure(f"obsolete parallel source remains: {obsolete.relative_to(PACKAGE)}")
            receipt = PACKAGE / "release" / "Vinci_TR3_PACKAGE_RECEIPT_v1.0.3.json"
            if json.loads(receipt.read_text(encoding="utf-8")) != expected_receipt(arxiv_pages):
                raise GateFailure("package receipt is stale; run source/rebuild_all.sh --write")

    verify_inventory(
        os.environ["REPORT_VERSION"],
        os.environ["PACKAGE_REVISION"],
        os.environ["PACKAGE_DIR_NAME"],
    )
    with tempfile.TemporaryDirectory(prefix="tr3-package.") as temp_name:
        archive = Path(temp_name) / f"{os.environ['ZIP_BASE']}.zip"
        deterministic_zip(PACKAGE, archive, prefix=os.environ["PACKAGE_DIR_NAME"])
        print(f"package_sha256={sha256(archive)}")
    print(f"historical_v1_pdf_sha256={sha256(historical_pdf)}")
    print(f"unpublished_candidate_pdf_sha256={sha256(REPORT / os.environ['CANDIDATE_PDF_NAME'])}")
    print(f"TR3 package authority: {args.mode} passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GateFailure as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
