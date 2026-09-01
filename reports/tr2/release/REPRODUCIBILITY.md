# Reproducibility Guide

## What this package can reproduce

This package can reproduce the manuscript, figures, aggregate tables, and package checksums from the included source files. It cannot yet independently recompute the scientific readout from item-level scored outputs because those private artifacts have not been exported into this package.

## What version 1.0 reproduces

Version 1.0 is an aggregate-only release. It reproduces the manuscript, figures, aggregate
tables, and package checksums from the included source files. It does not contain
item-level scored outputs, so an independent reader cannot recompute the scientific readout
from this package.

## What a complete public evidence release should reproduce

Items 3 to 6 below are not met by version 1.0. A complete public evidence release should
allow an independent reader to:

1. verify the validation-set SHA-256;
2. verify all public artifact hashes;
3. load sanitized item-level C0 and C3 scored outputs;
4. recompute per-family, per-judge UAR and ACC summaries;
5. apply the Judge-B-only refusal adjustment;
6. recompute the canonical G1 reliability artifact from frozen labels and locks;
7. reproduce every CSV and figure in this package;
8. confirm that the primary-test holdout remained sealed and was not included.

## Included build paths

From the package root:

```sh
python source/build_figures_and_tables.py
python source/make_pdf_source.py
python source/style_docx.py
```

Detailed dependency and build commands are in `source/BUILD.md`.

## Required frozen inputs for scientific recomputation

The public export should include, at minimum:

- sanitized scored C0/C3 rows;
- item IDs, pair IDs, answerability, family, condition, seed, and judge verdict fields;
- the exclusion/quarantine record;
- Judge-A and Judge-B canonical label files;
- sanitized per-call judge ledgers;
- gate analysis lock and artifact bindings;
- the frozen analysis scripts and registered package metadata;
- the validation manifest and licence record.

## Fail-closed rules

A reproduction must stop rather than emit a number when:

- any expected input is missing;
- an input hash differs from the frozen manifest;
- a judge ledger is missing, truncated, mixed-model, or echo-mismatched;
- a required field is blank;
- the validation set hash is wrong;
- a family, seed, condition, or declared judge is silently absent;
- primary-test content appears in the export.

## Execution provenance limitation

Every original execution manifest records `code_commit: unknown`. Report the content-addressed bundle digest as the execution source identity. Do not fill the missing Git field with the publication commit.
