#!/usr/bin/env bash
# Regenere toutes les figures et tous les tableaux du depot.
# Aucun acces reseau n'est necessaire si matplotlib est deja installe.
set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

if ! "$PYTHON" -c "import matplotlib" >/dev/null 2>&1; then
  if [ -x "$RACINE/.venv/bin/python" ]; then
    PYTHON="$RACINE/.venv/bin/python"
  else
    echo "matplotlib est absent : creation de .venv et installation des dependances." >&2
    python3 -m venv "$RACINE/.venv"
    "$RACINE/.venv/bin/pip" install --quiet --upgrade pip
    "$RACINE/.venv/bin/pip" install --quiet -r "$RACINE/code/requirements.txt"
    PYTHON="$RACINE/.venv/bin/python"
  fi
fi

if ! "$PYTHON" -c "import matplotlib" >/dev/null 2>&1; then
  echo "Impossible d'importer matplotlib avec $PYTHON." >&2
  echo "Installer matplotlib puis relancer : PYTHON=/chemin/python bash code/reproduire.sh" >&2
  exit 1
fi

mkdir -p "$RACINE/resultats/figures"
"$PYTHON" "$RACINE/code/analyser.py"
"$PYTHON" "$RACINE/code/tracer_resultats.py"

echo "Figures PDF et PNG :"
find "$RACINE/resultats/figures" -maxdepth 1 -type f \( -name '*.pdf' -o -name '*.png' \) -printf '  %f\n' | sort
