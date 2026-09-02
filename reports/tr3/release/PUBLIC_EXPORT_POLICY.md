# Public Export Policy

## Allowlist

The public bundle may include:

- the final report and its derived formats;
- aggregate metrics with exact numerator, denominator, unit, and derivation;
- scientific figures generated only from public aggregate values;
- evidence paths, commit IDs, blob SHAs, and stable GitHub commit URLs;
- claim-disposition records and correction history;
- build scripts, formatting sources, metadata, licences, and checksums;
- public communication copy that stays inside `release/CLAIMS.md`.

## Denylist

The public bundle must not include:

- protected, encrypted, or hidden task content;
- certification tests, custody registries, decryption keys, or access tokens;
- raw private model responses or unpublished traces;
- provider credentials, headers, request IDs, or unredacted API returns;
- model weights or adapters;
- personal data beyond the author’s public name and affiliation;
- a claim that an evaluator, model, or product passed when the final disposition says otherwise.

## Review rule

A file not explicitly covered by the allowlist is excluded until a human reviews it. Public convenience never overrides the protected-evidence boundary.
