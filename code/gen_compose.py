#!/usr/bin/env python3
"""Genere un docker-compose.yml pour n validateurs CometBFT.

Usage :
    python3 code/gen_compose.py 4 /chemin/absolu/vers/testnet
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

N = int(sys.argv[1]) if len(sys.argv) > 1 else 4
TESTNET = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path("testnet").resolve()
IMAGE = "cometbft/cometbft:v0.38.17"
PORT_RPC = os.environ.get("A9_RPC_PORT", "36657")

lignes = ["services:"]
for i in range(N):
    lignes += [
        f"  node{i}:",
        f"    image: {IMAGE}",
        f"    container_name: node{i}",
        f"    hostname: node{i}",
        "    user: root",
        '    entrypoint: ["cometbft"]',
        '    command: ["node", "--home", "/cometbft", "--proxy_app=kvstore", '
        '"--rpc.laddr=tcp://0.0.0.0:26657"]',
        f'    volumes: ["{TESTNET / f"node{i}"}:/cometbft"]',
    ]
    if i == 0:
        lignes.append(f'    ports: ["{PORT_RPC}:26657"]')
    lignes.append("")

(TESTNET / "docker-compose.yml").write_text("\n".join(lignes), encoding="utf-8")
print(f"{TESTNET / 'docker-compose.yml'} ecrit pour {N} noeuds")
