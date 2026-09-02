#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
PKG = ROOT / "reports" / "tr3"
BUILDER = PKG / "source" / "package_release.py"

spec = importlib.util.spec_from_file_location("tr3_package_release", BUILDER)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Tr3PackageAuthorityTest(unittest.TestCase):
    def test_positive_rebuild_reaches_every_surface_and_preserves_pdf(self) -> None:
        pdf = PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"
        before = digest(pdf)
        result = subprocess.run(
            ["bash", "source/rebuild_all.sh", "--write"],
            cwd=PKG,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TR3 package authority: write passed", result.stdout)
        self.assertEqual(digest(pdf), before)
        self.assertEqual((PKG / "source" / "report_body.md").read_bytes(), (PKG / "report" / "Vinci_Technical_Report_No_3.md").read_bytes())
        with zipfile.ZipFile(PKG / "report" / "Vinci_Technical_Report_No_3.docx") as archive:
            self.assertEqual(len([n for n in archive.namelist() if n.startswith("word/media/")]), 6)

    def test_restored_prepublication_marker_fails_the_intended_guard(self) -> None:
        contract = json.loads((PKG / "release" / "SEMANTIC_CONTRACT.json").read_text())
        stale = (PKG / "source" / "report_body.md").read_text() + "\nThis draft intentionally leaves that field unresolved.\n"
        with self.assertRaisesRegex(module.GateFailure, "forbidden pre-publication marker"):
            module.assert_contract_text("restored stale manuscript", stale, contract, require_all=True)

    def test_restored_stale_arxiv_archive_fails_the_intended_guard(self) -> None:
        contract = json.loads((PKG / "release" / "SEMANTIC_CONTRACT.json").read_text())
        stale = "Publication source commit: [TO BE FROZEN]\nFUNDING DISCLOSURE REQUIRED"
        with self.assertRaisesRegex(module.GateFailure, "TO BE FROZEN"):
            module.assert_contract_text("restored stale arXiv body", stale, contract, require_all=False)

    def test_old_head_rebuild_overwrites_pdf_but_current_builder_cannot(self) -> None:
        old = subprocess.run(
            ["git", "show", "128dea8b4013cdb3398c98edab5dc930e24c51d2:reports/tr3/source/rebuild_all.sh"],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout
        with tempfile.TemporaryDirectory(prefix="tr3-old-rebuild.") as temp_name:
            package = Path(temp_name) / "package"
            (package / "source").mkdir(parents=True)
            (package / "arxiv" / "source").mkdir(parents=True)
            (package / "report").mkdir(parents=True)
            (package / "source" / "rebuild_all.sh").write_bytes(old)
            (package / "source" / "build_figures.py").write_text("pass\n")
            (package / "source" / "report_body.md").write_text("fixture\n")
            (package / "source" / "report.css").write_text("")
            (package / "source" / "reference.docx").write_bytes(b"fixture")
            (package / "arxiv" / "source" / "main.tex").write_text("fixture\n")
            accepted = package / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"
            accepted.write_bytes(b"accepted-pdf")
            fake_bin = Path(temp_name) / "bin"
            fake_bin.mkdir()
            (fake_bin / "python3").write_text("#!/bin/sh\nexit 0\n")
            (fake_bin / "xelatex").write_text("#!/bin/sh\nprintf replacement-pdf > main.pdf\n")
            (fake_bin / "pandoc").write_text("#!/bin/sh\nexit 0\n")
            for command in fake_bin.iterdir():
                command.chmod(0o755)
            result = subprocess.run(
                ["bash", "source/rebuild_all.sh"],
                cwd=package,
                env={**os.environ, "PATH": f"{fake_bin}:{os.environ['PATH']}"},
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode())
            self.assertEqual(accepted.read_bytes(), b"replacement-pdf")

    def test_manifest_has_one_count_and_one_version_axis(self) -> None:
        manifest = json.loads((PKG / "MANIFEST.json").read_text())
        self.assertEqual(manifest["report_version"], "1.0")
        self.assertEqual(manifest["package_revision"], "1.0.3")
        self.assertEqual(manifest["file_count"], len(manifest["files"]))
        for obsolete in ("package_version", "version", "file_count_excluding_manifest_and_checksum_inventory"):
            self.assertNotIn(obsolete, manifest)

    def test_published_zenodo_record_is_not_a_staging_target(self) -> None:
        result = subprocess.run(
            ["bash", "scripts/zenodo_stage.sh", "tr3", "--dry-run"],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, "ZENODO_TOKEN_FILE": "/nonexistent"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no active Zenodo draft", result.stderr)
        self.assertNotIn("no token", result.stderr)


if __name__ == "__main__":
    unittest.main()
