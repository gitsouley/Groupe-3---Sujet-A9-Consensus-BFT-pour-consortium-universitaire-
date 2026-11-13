#!/usr/bin/env python3
"""Mesure la latence et le debit d'un noeud CometBFT via son RPC.

Usage :
    python3 code/mesure.py http://localhost:26657 20 200

Les deux nombres sont le nombre d'envois sequentiels pour la latence et le
nombre total d'envois pour le debit (20 envois simultanes).
"""

from __future__ import annotations

import json
import statistics
import sys
import time
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor

RPC = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:26657"
NLAT = int(sys.argv[2]) if len(sys.argv) > 2 else 20
NDEB = int(sys.argv[3]) if len(sys.argv) > 3 else 200
PAR = 20


def envoyer(_: object = None) -> tuple[float, bool]:
    tx = f"diplome-{uuid.uuid4().hex[:10]}=valide"
    url = f"{RPC}/broadcast_tx_commit?tx=%22{tx}%22"
    debut = time.perf_counter()
    try:
        with urllib.request.urlopen(url, timeout=15) as reponse:
            ok = "error" not in json.load(reponse)
    except Exception:
        ok = False
    return time.perf_counter() - debut, ok


def main() -> None:
    resultats = [envoyer() for _ in range(NLAT)]
    latences = sorted(duree * 1000 for duree, ok in resultats if ok)
    echecs = sum(1 for _, ok in resultats if not ok)
    if latences:
        p95 = latences[max(0, int(0.95 * len(latences)) - 1)]
        print(
            f"Latence (ms) : moyenne={statistics.mean(latences):.0f}  "
            f"mediane={statistics.median(latences):.0f}  p95={p95:.0f}  "
            f"echecs={echecs}/{NLAT}"
        )
    else:
        print(f"Latence : aucun envoi valide ({echecs}/{NLAT} echecs) -> chaine bloquee ?")

    debut = time.perf_counter()
    with ThreadPoolExecutor(PAR) as executeur:
        resultats = list(executeur.map(envoyer, range(NDEB)))
    duree = time.perf_counter() - debut
    ok = sum(1 for _, valide in resultats if valide)
    debit = ok / duree if duree else 0.0
    print(f"Debit : {ok}/{NDEB} valides en {duree:.1f} s -> {debit:.1f} tx/s")


if __name__ == "__main__":
    main()
