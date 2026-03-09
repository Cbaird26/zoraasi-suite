# Corpus Release Layout

This directory is the landing zone for the readable codex once sources are ingested and expanded from the registry.

## Target layout

```text
corpus-release/
  00_manifest/
    corpus_manifest.json
    source_hashes.csv
    document_versions.csv

  01_ingest/
    raw/
    extracted_txt/
    normalized_txt/

  02_chunks/
    doc_id/
      chunk_001_pages_001-010.txt
      chunk_001_analysis.json

  03_reconstruction/
    paper_001/
      reconstruction_full.md
      source_map.csv
      contradiction_log.md
      unresolved_gaps.md

  04_governance/
    canonical_status.md
    glossary.md
    notation.md
    claims_taxonomy.md
    contradiction_ledger.csv
    claims_registry.csv

  05_edit_pass/
    paper_001/
      edited_clean.md
      redline.md
      edit_log.md
      open_questions.md

  06_final_papers/
    paper_001_final.md
    paper_001_final.txt

  07_codex/
    master_codex.md
    master_codex.txt
    index.json
    paper_index.csv
    topic_index.csv
    equation_index.csv
    term_index.csv

  08_review/
    referee_pack.md
    evidence_trail.md
    publication_checklist.md
```

## Rule of order

Preserve first, reconstruct second, reduce last.
