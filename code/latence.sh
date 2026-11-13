#!/usr/bin/env bash
# Injecte ou retire une latence sur les conteneurs node0..node9.
# Usage : bash code/latence.sh on | bash code/latence.sh off
set -euo pipefail

declare -A RETARD=(
  [node0]=10
  [node1]=15
  [node2]=40
  [node3]=35
  [node4]=40
  [node5]=45
  [node6]=35
  [node7]=35
  [node8]=20
  [node9]=15
)

for noeud in "${!RETARD[@]}"; do
  docker inspect "$noeud" >/dev/null 2>&1 || continue
  if [ "${1:-}" = "on" ]; then
    docker run --rm --net "container:$noeud" --cap-add NET_ADMIN nicolaka/netshoot \
      tc qdisc replace dev eth0 root netem delay "${RETARD[$noeud]}ms" 5ms >/dev/null
    echo "$noeud : +${RETARD[$noeud]} ms (+/- 5 ms)"
  else
    docker run --rm --net "container:$noeud" --cap-add NET_ADMIN nicolaka/netshoot \
      tc qdisc del dev eth0 root 2>/dev/null || true
    echo "$noeud : retard retire"
  fi
done
