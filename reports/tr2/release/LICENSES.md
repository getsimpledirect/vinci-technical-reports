# Licensing Plan and Rights Review

**Status:** draft; final licences have not been assigned in version 0.9.

## Proposed release licences

| Artifact class | Proposed licence | Publication status |
|---|---|---|
| Technical report text | CC BY 4.0 | George to confirm before version 1.0 |
| Original figures | CC BY 4.0 | George to confirm before version 1.0 |
| Aggregate tables authored by Vinci | CC BY 4.0 | George to confirm before version 1.0 |
| Original analysis/build code | Apache 2.0 | Confirm repository compatibility |
| Validation benchmark items | Per-item rights decision required | Do not publish until audited |
| Sanitized model-judge labels/metadata | Rights and privacy review required | Do not publish until audited |
| Model weights/adapters | Not included | No licence decision required for this release |

## Upstream materials

This package names upstream model checkpoints but does not redistribute their weights. Each model remains governed by its upstream licence and model card. Public documentation should link to the exact pinned upstream revision rather than copying weight files into the report bundle.

## Benchmark rights gate

Before publishing the validation benchmark, assign every item one of:

- original Vinci-authored and releasable;
- derived from a source with compatible redistribution rights;
- releasable only with citation or limited fields;
- controlled access;
- excluded from the public set.

The rights audit must be bound to the exact public item hashes. A generic statement about the corpus is not enough.

## No automatic licence inheritance

Do not assume that the licence of the repository, base model, prompt source, or generated response automatically governs every benchmark item or judge output. Record licences by artifact class and item where needed.
