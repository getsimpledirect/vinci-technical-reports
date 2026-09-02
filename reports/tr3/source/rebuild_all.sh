#!/usr/bin/env bash
# Deterministic repository-forward TR3 builder. It cannot replace the frozen
# historical PDF and contains no network, upload, tag, release, or publication operation.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MODE="${1:---check}"
case "$MODE" in
  --check) MODE=check ;;
  --write) MODE=write ;;
  *) echo "usage: source/rebuild_all.sh [--check|--write]" >&2; exit 2 ;;
esac

# shellcheck disable=SC1091
source "$ROOT/release.conf"
export REPORT_VERSION PACKAGE_REVISION PACKAGE_DIR_NAME ARXIV_ZIP_NAME
export HISTORICAL_PDF_SHA256 HISTORICAL_PDF_NAME CANDIDATE_PDF_NAME ZIP_BASE
exec python3 "$ROOT/source/package_release.py" "$MODE"
