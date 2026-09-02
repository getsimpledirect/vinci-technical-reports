#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import copy
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
    def test_positive_rebuild_reaches_every_surface_and_preserves_historical_pdf(self) -> None:
        historical = PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"
        candidate = PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf"
        before = digest(historical)
        result = subprocess.run(
            ["bash", "source/rebuild_all.sh", "--write"],
            cwd=PKG,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TR3 package authority: write passed", result.stdout)
        self.assertEqual(digest(historical), before)
        self.assertTrue(candidate.is_file())
        self.assertNotEqual(digest(candidate), before)
        self.assertEqual((PKG / "source" / "report_body.md").read_bytes(), (PKG / "report" / "Vinci_Technical_Report_No_3.md").read_bytes())
        with zipfile.ZipFile(PKG / "report" / "Vinci_Technical_Report_No_3.docx") as archive:
            self.assertEqual(len([n for n in archive.namelist() if n.startswith("word/media/")]), 6)

    def test_restored_prepublication_marker_fails_the_intended_guard(self) -> None:
        contract = json.loads((PKG / "release" / "SEMANTIC_CONTRACT.json").read_text())
        stale = (PKG / "source" / "report_body.md").read_text() + "\nThis draft intentionally leaves that field unresolved.\n"
        with self.assertRaisesRegex(module.GateFailure, "forbidden pre-publication marker"):
            module.assert_contract_text("restored stale manuscript", stale, contract, require_all=True)

    def test_exact_blocked_head_fails_for_each_residual_finalization_mechanism(self) -> None:
        contract = json.loads((PKG / "release" / "SEMANTIC_CONTRACT.json").read_text())
        old_head = subprocess.run(
            [
                "git",
                "show",
                "4b2a8f93c48482eb7f88222474bac25ac0f8089f:reports/tr3/source/report_body.md",
            ],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        residuals = [item["marker"] for item in contract["known_historical_v1_pdf_divergence"]]
        with self.assertRaisesRegex(module.GateFailure, "forbidden pre-publication marker"):
            module.assert_contract_text("exact blocked head", old_head, contract, require_all=True)
        for marker in residuals:
            with self.subTest(marker=marker):
                self.assertIn(module.normalized(marker), module.normalized(old_head))
                with self.assertRaisesRegex(module.GateFailure, "forbidden pre-publication marker"):
                    module.assert_contract_text(
                        "restored exact residual", marker, contract, require_all=False
                    )

    def test_historical_pdf_is_disclosed_not_misclassified_as_corrected(self) -> None:
        contract = json.loads((PKG / "release" / "SEMANTIC_CONTRACT.json").read_text())
        historical = subprocess.run(
            ["pdftotext", str(PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"), "-"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        candidate = subprocess.run(
            ["pdftotext", str(PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf"), "-"],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout
        with self.assertRaisesRegex(module.GateFailure, "forbidden pre-publication marker"):
            module.assert_contract_text("historical v1.0", historical, contract, require_all=True)
        module.assert_contract_text("unpublished corrected candidate", candidate, contract, require_all=True)

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

    def test_assembly_refuses_rebuilt_pdf_that_no_longer_matches_the_gated_digest(self) -> None:
        """scripts/assemble_release.sh gates the supplied candidate, then rebuilds.

        The rebuild regenerates the candidate from the manuscript, so a manuscript
        that drifted from the approved candidate yields different bytes AFTER the
        gate. Before the repair the archive shipped those bytes under the old
        digest (review R9, finding 1). The gate must apply to the bytes that enter
        the archive: refuse, name the mechanism, write no archive. The unmodified
        tree is the positive control through the same entry point.
        """
        conf = (PKG / "release.conf").read_text()
        gated = conf.split('ASSEMBLY_PDF_SHA256="')[1].split('"')[0]
        with tempfile.TemporaryDirectory(prefix="tr3-assembly-gate.") as temp_name:
            root = Path(temp_name) / "repo"
            shutil.copytree(ROOT / "scripts", root / "scripts")
            shutil.copytree(PKG, root / "reports" / "tr3", ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
            candidate = root / "reports" / "tr3" / "report" / os.environ.get("CANDIDATE_PDF_NAME", "Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf")
            historical = root / "reports" / "tr3" / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"
            command = ["bash", "scripts/assemble_release.sh", "tr3", str(candidate.relative_to(root))]
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

            positive = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(positive.returncode, 0, positive.stdout + positive.stderr)
            self.assertIn(f"assembly PDF unchanged by rebuild ({gated})", positive.stdout)
            self.assertEqual(digest(candidate), gated)
            self.assertTrue(list((root / "dist").glob("*.zip")), "positive control must write the archive")

            manuscript = root / "reports" / "tr3" / "source" / "report_body.md"
            manuscript.write_text(manuscript.read_text() + "\nThis sentence exists only in the mutation control.\n")
            mutated = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertNotEqual(mutated.returncode, 0)
            self.assertIn("rebuild changed the assembly PDF", mutated.stderr)
            self.assertIn(f"not the gated {gated}", mutated.stderr)
            self.assertNotEqual(digest(candidate), gated, "the drifted manuscript must actually produce different bytes")
            self.assertEqual(list((root / "dist").glob("*.zip*")), [], "a refused assembly must leave no archive, not even the earlier one")
            self.assertEqual(digest(historical), os.environ.get("HISTORICAL_PDF_SHA256", digest(PKG / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf")))

    def test_assembly_refuses_rebuildable_package_with_no_approval_digest(self) -> None:
        """An empty or unset ASSEMBLY_PDF_SHA256 must refuse, not degrade.

        Before the repair an empty digest skipped the step-1 comparison and the
        post-rebuild gate compared the rebuilt bytes against whatever was handed
        in: a drifted, unapproved rebuild assembled with exit 0 and a ZIP and no
        line said that nothing had been approved (review R13, finding N1). For a
        package with a rebuild path the absence of a digest must be the refusal,
        named as such, before any other gate runs and before any archive exists.
        The configured digest, and the ACCEPTED_PDF_SHA256 fallback, remain the
        positive controls through the same entry point.
        """
        conf_text = (PKG / "release.conf").read_text()
        gated = conf_text.split('ASSEMBLY_PDF_SHA256="')[1].split('"')[0]
        configured_line = f'ASSEMBLY_PDF_SHA256="{gated}"'
        self.assertIn(configured_line, conf_text)
        with tempfile.TemporaryDirectory(prefix="tr3-assembly-digest.") as temp_name:
            root = Path(temp_name) / "repo"
            shutil.copytree(ROOT / "scripts", root / "scripts")
            shutil.copytree(PKG, root / "reports" / "tr3", ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
            package = root / "reports" / "tr3"
            conf = package / "release.conf"
            candidate = package / "report" / "Vinci_Technical_Report_No_3_v1.0.3-candidate.pdf"
            historical = package / "report" / "Vinci_Technical_Report_No_3_v1.0.pdf"
            historical_before = digest(historical)
            self.assertTrue((package / "source" / "rebuild_all.sh").exists(), "this control needs a rebuild path")
            command = ["bash", "scripts/assemble_release.sh", "tr3", str(candidate.relative_to(root))]
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}

            for label, replacement in [
                ("empty", 'ASSEMBLY_PDF_SHA256=""'),
                ("unset", "# ASSEMBLY_PDF_SHA256 deliberately absent in this control"),
            ]:
                with self.subTest(digest=label):
                    conf.write_text(conf_text.replace(configured_line, replacement))
                    refused = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.assertNotEqual(refused.returncode, 0, "no configured digest must refuse, not assemble")
                    self.assertIn("no ASSEMBLY_PDF_SHA256 configured", refused.stderr)
                    self.assertIn("nothing approves these bytes", refused.stderr)
                    self.assertNotIn("  ok   ", refused.stdout, "the digest absence must be the first refusal, not a later gate")
                    self.assertNotIn("== 2.", refused.stdout, "the rebuild must not run without an approval digest")
                    self.assertEqual(list((root / "dist").glob("*.zip*")), [], "a refused assembly must leave no archive")
                    self.assertEqual(digest(candidate), gated, "the candidate must not be regenerated by a refused run")

            for label, replacement in [
                ("configured", configured_line),
                ("accepted-fallback", f'ACCEPTED_PDF_SHA256="{gated}"'),
            ]:
                with self.subTest(digest=label):
                    conf.write_text(conf_text.replace(configured_line, replacement))
                    positive = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.assertEqual(positive.returncode, 0, positive.stdout + positive.stderr)
                    self.assertNotIn("no ASSEMBLY_PDF_SHA256 configured", positive.stderr)
                    self.assertIn(f"assembly PDF unchanged by rebuild ({gated})", positive.stdout)
                    self.assertEqual(digest(candidate), gated)
                    self.assertTrue(list((root / "dist").glob("*.zip")), "positive control must write the archive")
            self.assertEqual(digest(historical), historical_before)

    def test_manifest_has_one_count_and_one_version_axis(self) -> None:
        manifest = json.loads((PKG / "MANIFEST.json").read_text())
        self.assertEqual(manifest["report_version"], "1.0")
        self.assertEqual(manifest["package_revision"], "1.0.3")
        self.assertEqual(manifest["file_count"], len(manifest["files"]))
        self.assertEqual(
            manifest["historical_pdf_sha256"],
            "054a4077193a797e8105224e710b0fc78741eb3f465ce1f994d9a1e960a32e1d",
        )
        for obsolete in ("package_version", "version", "file_count_excluding_manifest_and_checksum_inventory"):
            self.assertNotIn(obsolete, manifest)

    def test_inventory_rejects_duplicate_manifest_entry(self) -> None:
        data, expected = self._manifest_fixture()
        data["files"].append(copy.deepcopy(data["files"][0]))
        with self.assertRaisesRegex(module.GateFailure, "duplicate manifest path"):
            module.parse_manifest(data, expected)

    def test_inventory_rejects_duplicate_checksum_row(self) -> None:
        text = (PKG / "CHECKSUMS.sha256").read_text()
        duplicate = text + text.splitlines()[0] + "\n"
        with self.assertRaisesRegex(module.GateFailure, "duplicate checksum path"):
            module.parse_checksums(duplicate)

    def test_inventory_rejects_missing_required_metadata(self) -> None:
        required = [
            "schema_version",
            "publication_record",
            "publication_source_commit",
            "inventory_excludes",
        ]
        for key in required:
            with self.subTest(key=key):
                data, expected = self._manifest_fixture()
                del data[key]
                with self.assertRaisesRegex(module.GateFailure, "missing required field"):
                    module.parse_manifest(data, expected)

    def test_inventory_rejects_wrong_metadata_types(self) -> None:
        for key, value, message in [
            ("schema_version", "1", "schema_version must be integer 1"),
            ("schema_version", True, "schema_version must be integer 1"),
            ("inventory_excludes", "MANIFEST.json", "inventory_excludes must be a list"),
            ("inventory_excludes", ["MANIFEST.json", 3], "inventory_excludes must be a list"),
        ]:
            with self.subTest(key=key, value=value):
                data, expected = self._manifest_fixture()
                data[key] = value
                with self.assertRaisesRegex(module.GateFailure, message):
                    module.parse_manifest(data, expected)

    def test_packaged_source_executes_same_positive_rebuild_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tr3-package-parity.") as temp_name:
            archive = Path(temp_name) / "package.zip"
            module.deterministic_zip(PKG, archive, prefix="packaged-tr3")
            with zipfile.ZipFile(archive) as packaged:
                packaged.extractall(Path(temp_name) / "unpacked")
            packaged_root = Path(temp_name) / "unpacked" / "packaged-tr3"
            result = subprocess.run(
                ["bash", "source/rebuild_all.sh", "--check"],
                cwd=packaged_root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("TR3 package authority: check passed", result.stdout)
            self.assertEqual(
                (PKG / "source" / "package_release.py").read_bytes(),
                (packaged_root / "source" / "package_release.py").read_bytes(),
            )

    @staticmethod
    def _manifest_fixture() -> tuple[dict, dict]:
        data = json.loads((PKG / "MANIFEST.json").read_text())
        expected = {
            key: copy.deepcopy(data[key])
            for key in [
                "schema_version",
                "report_version",
                "package_revision",
                "package",
                "publication_record",
                "publication_source_commit",
                "source_authority",
                "historical_pdf_sha256",
                "inventory_excludes",
            ]
        }
        return data, expected

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
