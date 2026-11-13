#!/usr/bin/env bash
# Rejoue les scenarios CometBFT sur un reseau de test Docker.
# Usage : bash code/experimenter.sh [4|7|10] [--pannes] [--keep]
set -euo pipefail

RACINE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
N="${1:-4}"
shift || true
PANNES=0
KEEP=0
for option in "$@"; do
  case "$option" in
    --pannes) PANNES=1 ;;
    --keep) KEEP=1 ;;
    *) echo "Option inconnue : $option" >&2; exit 2 ;;
  esac
done

case "$N" in
  4|7|10) ;;
  *) echo "N doit valoir 4, 7 ou 10." >&2; exit 2 ;;
esac

IMG="cometbft/cometbft:v0.38.17"
PORT="${A9_RPC_PORT:-36657}"
PROJET="a9n${N}"
DIR="${A9_TESTNET_DIR:-$(mktemp -d "/tmp/a9_n${N}.XXXXXX")}"
LOG="${RACINE}/resultats/journal_experience_n${N}.log"

mkdir -p "$(dirname "$LOG")"
exec > >(tee -a "$LOG") 2>&1

echo "== Reseau n=${N} =="
echo "Dossier testnet : $DIR"
echo "RPC : http://localhost:${PORT}"

if ! docker image inspect "$IMG" >/dev/null 2>&1; then
  echo "Image absente : docker pull $IMG"
  docker pull "$IMG"
fi
if ! docker image inspect nicolaka/netshoot >/dev/null 2>&1; then
  docker pull nicolaka/netshoot
fi

docker run --rm --user root -v "${DIR}:/cometbft" "$IMG" testnet --v "$N" --o /cometbft
A9_RPC_PORT="$PORT" python3 "${RACINE}/code/gen_compose.py" "$N" "$DIR"
docker compose -f "${DIR}/docker-compose.yml" -p "$PROJET" up -d

echo "Attente du premier bloc..."
for _ in $(seq 1 60); do
  sleep 2
  if curl -sf "http://localhost:${PORT}/status" \
      | python3 -c "import json,sys; d=json.load(sys.stdin); raise SystemExit(0 if int(d['result']['sync_info']['latest_block_height'])>1 else 1)" 2>/dev/null; then
    break
  fi
done
curl -s "http://localhost:${PORT}/validators" \
  | python3 -c "import json,sys; v=json.load(sys.stdin)['result']['validators']; print(f'Validateurs actifs : {len(v)}')"

bash "${RACINE}/code/latence.sh" on

echo "== S1/S2/S3 : trois essais de latence et de debit =="
for essai in 1 2 3; do
  echo "-- essai ${essai} --"
  python3 "${RACINE}/code/mesure.py" "http://localhost:${PORT}" 20 200
done

if [ "$PANNES" -eq 1 ]; then
  F=$(( (N - 1) / 3 ))
  echo "== S4 : arret de f = ${F} validateur(s) =="
  for i in $(seq 1 "$F"); do
    docker stop "node$((N - i))" >/dev/null
  done
  sleep 5
  python3 "${RACINE}/code/mesure.py" "http://localhost:${PORT}" 10 50

  echo "== S4 : arret de f + 1 = $((F + 1)) validateur(s) =="
  docker stop "node$((N - F - 1))" >/dev/null
  sleep 5
  python3 "${RACINE}/code/mesure.py" "http://localhost:${PORT}" 10 10 || true

  echo "== Redemarrage des validateurs =="
  for i in $(seq 0 $((F))); do
    docker start "node$((N - F - 1 + i))" >/dev/null
  done
  sleep 12
  python3 "${RACINE}/code/mesure.py" "http://localhost:${PORT}" 10 50
fi

if [ "$KEEP" -eq 0 ]; then
  echo "Arret du reseau. Les fichiers de $DIR restent dans /tmp (racine)."
  docker compose -f "${DIR}/docker-compose.yml" -p "$PROJET" down
fi

echo "Journal : $LOG"
