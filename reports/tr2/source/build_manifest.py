#!/usr/bin/env python3
"""Build the Vinci TR2 package manifest and SHA-256 checksum file.

Run from anywhere. The package root is inferred from this script's location.
The manifest deliberately excludes itself and checksums.sha256 to avoid
self-reference. checksums.sha256 includes manifest.json and every other
packaged file except itself.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
CHECKSUMS = ROOT / "checksums.sha256"
EXCLUDED_PARTS = {"qa", "__pycache__", ".git"}
EXCLUDED_SUFFIXES = {".aux", ".log", ".out", ".toc", ".synctex.gz", ".tmp"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def eligible_files() -> Iterable[Path]:
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if any(path.name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES):
            continue
        yield path


def main() -> None:
    files_for_manifest = [
        path for path in eligible_files()
        if path not in {MANIFEST, CHECKSUMS}
    ]
    manifest = {
        "schema": "vinci-publication-package-manifest/v1",
        "package": "Vinci Technical Report No. 2 - Character Transfer Across Three Model Families",
        "package_version": "0.9",
        "evidence_tier": "development",
        "claim_tier": "internal-review-only",
        "primary_test_holdout": "untouched",
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "file_count": len(files_for_manifest),
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
            for path in files_for_manifest
        ],
        "integrity_note": (
            "manifest.json excludes itself and checksums.sha256. "
            "checksums.sha256 includes manifest.json and all other packaged files except itself."
        ),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    files_for_checksums = [path for path in eligible_files() if path != CHECKSUMS]
    lines = [
        f"{sha256_file(path)}  {path.relative_to(ROOT).as_posix()}"
        for path in files_for_checksums
    ]
    CHECKSUMS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} ({len(files_for_manifest)} files)")
    print(f"wrote {CHECKSUMS} ({len(files_for_checksums)} checksums)")


if __name__ == "__main__":
    main()
