# Build

From the package root:

```sh
bash source/rebuild_all.sh
```

This regenerates the six figures, XeLaTeX PDF, self-contained HTML, and editable DOCX from included public sources. It does not require private task content or raw model outputs.

`source/build_release_reference.py` is the exact environment-specific orchestration script used to assemble this complete release package. It is preserved for audit, not as the portable entry point.

After any change, regenerate `MANIFEST.json` and `CHECKSUMS.sha256`, then rebuild the detached package ZIP hash.
