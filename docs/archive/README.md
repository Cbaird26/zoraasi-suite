# Corpus Archive Scaffold

This directory holds the preservation-first scaffold for rebuilding the Theory of Everything corpus into readable, traceable editions.

## Why this exists

The repo already tracks repositories by rollout wave, but it does not yet track individual papers, page ranges, or reconstructed editions. This scaffold fills that gap without pulling sealed material into the public repo.

## Current scope

- `corpus_manifest.json` is the machine-readable registry.
- `CORPUS_INDEX.md` is the generated human-readable record list.
- `CORPUS_CHRONOLOGY.md` is the generated chronological reading aid.
- `templates/` holds the working files for chunking, source maps, contradictions, and claim status.

Right now the manifest is seeded at the collection level from:

- `docs/ops/CB26_WAVE2_PUBLIC_TRACKER.md`
- `docs/ops/CB26_WAVE3_ARCHIVE_TRACKER.md`
- `identity/INNER_REFERENCE.md`

That means each repo or private pointer is only a starting record. Expand each one into document-level entries before heavy editing begins.

## Edition model

Use the same four edition targets across the corpus:

1. `pull_page_full_reading`
   - Full reading copy.
   - Preserve original order inside each source.
   - Allow only OCR cleanup, dehyphenation, and obvious scan cleanup.
2. `chronological_full`
   - Same corpus, ordered by exact or inferred date.
   - Label inferred dates explicitly.
3. `paper_reconstruction`
   - One coherent reconstruction per scientific paper.
   - Keep source maps and contradiction logs adjacent to the reconstructed text.
4. `clean_editorial`
   - Later reduction pass.
   - Never start here.

## Recommended workflow

1. Run `python3 scripts/ops/generate_corpus_docs.py`.
2. Expand `corpus_manifest.json` from repo collections into source documents.
3. Ingest each source into the `corpus-release/` structure.
4. Create the pull-page full reading edition first.
5. Create the chronological edition second.
6. Reconstruct each paper third.
7. Only then run trimming and consistency passes.

## Public/private boundary

Records marked `private_workspace_only` are pointers only in this repo. Build their full reading copies in the private workspace, not here.
