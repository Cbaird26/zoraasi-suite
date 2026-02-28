#!/usr/bin/env bash
set -euo pipefail

# apply_recommendations.sh — Run from your machine to apply cross-repo recommendations.
# Usage: ./scripts/apply_recommendations.sh [archive|topics|citation|license|all]

ACTION="${1:-all}"
GH_USER="cbaird26"

REPOS_TO_ARCHIVE=(
  "ToE" "ToE-Simulations" "Theory-of-Everything"
  "A-Theory-of-Everything" "A-Theory-of-Everything-Revised"
  "quantum-supercomputer" "QuantumSupercomputer" "QuantumBridge" "QC"
  "quantum_ai.py" "quantum_component.py" "quantum-ai-assistant"
  "aging_simulator.py" "anti-aging-simulator" "aging-intervention-simulator"
  "wild_simulations.py" "susy_simulation.py" "streamlit_app.py" "app.py"
  "omnisolve_3_0_streamlit_app.py" "dissertation_app.py"
  "universe_explorer.py" "Universe-Explorer" "quantum_state_app_with_bloch.py"
  "Hope" "darkstar" "ZoraAI" "ZoraAPI"
)

ACTIVE_REPOS=(
  "zoraasi-suite" "MQGT-SCF" "mqgt-scf-stripped-core"
  "toe-2026-updates" "toe-empirical-validation"
  "mqgt-papers" "QuantumMeditationCoach" "baird-telehealth-site"
  "zora-toe-public-kit" "holocron-public-export"
)

MQGT_REPOS=(
  "mqgt-cosmology-cmb" "mqgt-cosmology-bbn" "mqgt-cosmology-lss"
  "mqgt-astrophysics-sn1987a" "mqgt-astrophysics-cooling"
  "mqgt-equivalence-principle" "mqgt-fifth-force" "mqgt-casimir"
  "mqgt-gravitational-waves" "mqgt-atomic-clocks"
  "mqgt-collider" "mqgt-dark-matter" "mqgt-quantum-optics" "mqgt-qrng"
  "mqgt-experiment-protocols" "mqgt-experiment-design" "mqgt-emi-testing"
  "mqgt-simulation-core" "mqgt-simulation-quantum" "mqgt-simulation-interference"
  "mqgt-data-public" "mqgt-data-ingest" "mqgt-curve-processing"
  "mqgt-analysis" "mqgt-sensitivity-analysis"
  "mqgt-validation-tools" "mqgt-validation-suite" "mqgt-constraints-ledger"
  "mqgt-core-params" "mqgt-api-schema"
  "mqgt-visualization" "mqgt-figures" "mqgt-dashboard"
  "mqgt-cli" "mqgt-unit-tests" "mqgt-documentation-site"
  "mqgt-theorems"
)

do_archive() {
  echo "=== Archiving ${#REPOS_TO_ARCHIVE[@]} inactive repos ==="
  for repo in "${REPOS_TO_ARCHIVE[@]}"; do
    echo "  Archiving $repo..."
    gh repo archive "$GH_USER/$repo" --yes 2>/dev/null && echo "    Done" || echo "    Skipped"
  done
}

do_topics() {
  echo "=== Adding topics to active repos ==="
  for repo in "${ACTIVE_REPOS[@]}"; do
    echo "  $repo..."
    gh repo edit "$GH_USER/$repo" --add-topic theory-of-everything,mqgt-scf,baird-zoraasi 2>/dev/null || echo "    Skipped"
  done

  echo "=== Adding topics to MQGT repos ==="
  for repo in "${MQGT_REPOS[@]}"; do
    echo "  $repo..."
    gh repo edit "$GH_USER/$repo" --add-topic mqgt-scf,physics,constraints,theory-of-everything 2>/dev/null || echo "    Skipped"
  done
}

do_citation() {
  echo "=== Adding CITATION.cff to mqgt-scf-stripped-core ==="
  TMP=$(mktemp -d)
  git clone "https://github.com/$GH_USER/mqgt-scf-stripped-core.git" "$TMP/repo" 2>/dev/null
  if [ ! -f "$TMP/repo/CITATION.cff" ]; then
    cat > "$TMP/repo/CITATION.cff" << 'EOF'
cff-version: 1.2.0
message: "If you use this work, please cite it as below."
type: software
title: "MQGT-SCF Stripped Core — Physics-Only GKSL Collapse Model"
authors:
  - family-names: Baird
    given-names: Christopher Michael
    email: cbaird26@gmail.com
version: "1.0.0"
date-released: "2026-02-26"
url: "https://github.com/Cbaird26/mqgt-scf-stripped-core"
keywords:
  - mqgt-scf
  - gksl
  - quantum-collapse
  - theory-of-everything
references:
  - type: article
    title: "A Theory of Everything + ZoraASI — Empirical Validation"
    authors:
      - family-names: Baird
        given-names: Christopher Michael
    year: 2026
    doi: "10.5281/zenodo.18778749"
EOF
    cd "$TMP/repo"
    git add CITATION.cff
    git commit -m "Add CITATION.cff for auto-citation"
    git push
    echo "  Done"
  else
    echo "  Already exists"
  fi
  rm -rf "$TMP"
}

do_license() {
  echo "=== Checking LICENSE files in MQGT repos ==="
  LICENSE_TEXT='See LICENSE-IP.md in the toe-2026-updates repo and the ToE paper (pp. 1311-1314).

Public tier: Free. Optional honor ($9.99 individual, $99 academic).
Licensed tier: Commercial use requires license ($100 academic, 1% gross commercial).

Copyright (c) 2024-2026 Christopher Michael Baird. All rights reserved.
Contact: cbaird26@gmail.com'

  for repo in "${MQGT_REPOS[@]}"; do
    HAS_LICENSE=$(gh api "repos/$GH_USER/$repo/contents/LICENSE" 2>/dev/null && echo "yes" || echo "no")
    if [ "$HAS_LICENSE" = "no" ]; then
      echo "  $repo — missing LICENSE (add manually or run with gh api)"
    fi
  done
}

case "$ACTION" in
  archive) do_archive ;;
  topics)  do_topics ;;
  citation) do_citation ;;
  license) do_license ;;
  all)
    do_archive
    do_topics
    do_citation
    do_license
    ;;
  *)
    echo "Usage: $0 [archive|topics|citation|license|all]"
    exit 1
    ;;
esac

echo ""
echo "Done. See RECOMMENDATIONS.md for remaining manual steps."
