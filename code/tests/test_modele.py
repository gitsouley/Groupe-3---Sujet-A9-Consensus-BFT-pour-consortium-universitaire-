"""Tests unitaires du modele BFT et de l'agregation des mesures."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RACINE / "code"))

from analyser import parametres  # noqa: E402
from tracer_resultats import agreger  # noqa: E402


class TestParametresBFT(unittest.TestCase):
    def test_configurations_mesurees(self) -> None:
        attendus = {
            4: (1, 3, 28),
            7: (2, 5, 91),
            10: (3, 7, 190),
        }
        for n, (f, quorum, messages) in attendus.items():
            p = parametres(n)
            self.assertEqual(p["f"], f)
            self.assertEqual(p["quorum"], quorum)
            self.assertEqual(p["messages"], messages)

    def test_seuil_et_intersection(self) -> None:
        for n in range(4, 21):
            p = parametres(n)
            self.assertGreaterEqual(n, 3 * p["f"] + 1)
            self.assertEqual(p["intersection"], max(0, 2 * p["quorum"] - n))
        for n in (4, 7, 10):
            p = parametres(n)
            self.assertEqual(p["intersection"], p["f"] + 1)

    def test_formule_messages(self) -> None:
        for n in range(4, 21):
            self.assertEqual(parametres(n)["messages"], 2 * n * n - n)


class TestAgregation(unittest.TestCase):
    def test_moyenne_et_statut(self) -> None:
        lignes = [
            {
                "scenario": "S1",
                "n": "4",
                "panne": "0",
                "latence_moy_ms": "1000",
                "p95_ms": "1100",
                "debit_tx_s": "10",
                "tx_ok": "20",
                "tx_total": "20",
            },
            {
                "scenario": "S1",
                "n": "4",
                "panne": "0",
                "latence_moy_ms": "1200",
                "p95_ms": "1300",
                "debit_tx_s": "11",
                "tx_ok": "20",
                "tx_total": "20",
            },
        ]
        agregats = agreger(lignes)
        self.assertEqual(len(agregats), 1)
        self.assertEqual(agregats[0]["latence_moy_ms"], 1100.0)
        self.assertEqual(agregats[0]["statut"], "operationnel")
        self.assertEqual(agregats[0]["tx_ok"], 40)

    def test_blocage(self) -> None:
        lignes = [
            {
                "scenario": "S4",
                "n": "4",
                "panne": "2",
                "latence_moy_ms": "",
                "p95_ms": "",
                "debit_tx_s": "0",
                "tx_ok": "0",
                "tx_total": "3",
            }
        ]
        agregats = agreger(lignes)
        self.assertEqual(agregats[0]["statut"], "bloque")
        self.assertIsNone(agregats[0]["latence_moy_ms"])


if __name__ == "__main__":
    unittest.main()
