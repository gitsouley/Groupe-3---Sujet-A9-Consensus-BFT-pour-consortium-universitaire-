#!/usr/bin/env python3
"""Agrege les mesures CometBFT et produit les figures 3, 4 et 5.

Entrees  : resultats/mesures_brutes.csv, resultats/timeline_pannes.csv
Sorties  : resultats/mesures_agregees.csv, resultats/figures/fig3_*.pdf,
           resultats/figures/fig4_*.pdf, resultats/figures/fig5_*.pdf
"""

from __future__ import annotations

import csv
import math
import statistics
from collections import OrderedDict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RACINE = Path(__file__).resolve().parents[1]
RESULTATS = RACINE / "resultats"
FIGURES = RESULTATS / "figures"
FIGURES.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "legend.fontsize": 8,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.dpi": 300,
        "figure.dpi": 150,
    }
)

BLEU = "#1f4e79"
ORANGE = "#c55a11"
VERT = "#548235"
GRIS = "#595959"
ROUGE = "#a61c00"


def nombre(valeur: str) -> float | None:
    valeur = (valeur or "").strip()
    if not valeur:
        return None
    try:
        return float(valeur)
    except ValueError:
        return None


def charger_mesures() -> list[dict[str, str]]:
    with (RESULTATS / "mesures_brutes.csv").open(encoding="utf-8") as flux:
        return list(csv.DictReader(flux))


def agreger(lignes: list[dict[str, str]]) -> list[dict[str, object]]:
    groupes: OrderedDict[tuple[str, str, str], list[dict[str, str]]] = OrderedDict()
    for ligne in lignes:
        cle = (ligne["scenario"], ligne["n"], ligne["panne"])
        groupes.setdefault(cle, []).append(ligne)

    agregats: list[dict[str, object]] = []
    for (scenario, n, panne), essais in groupes.items():
        latences = [nombre(e["latence_moy_ms"]) for e in essais]
        latences = [v for v in latences if v is not None]
        p95 = [nombre(e["p95_ms"]) for e in essais]
        p95 = [v for v in p95 if v is not None]
        debits = [nombre(e["debit_tx_s"]) for e in essais]
        debits = [v for v in debits if v is not None]
        tx_ok = sum(int(e["tx_ok"] or 0) for e in essais)
        tx_total = sum(int(e["tx_total"] or 0) for e in essais)
        bloque = not latences
        if latences:
            moyenne = statistics.mean(latences)
            ecart = statistics.stdev(latences) if len(latences) > 1 else 0.0
            ic95 = 4.303 * ecart / math.sqrt(len(latences)) if len(latences) > 1 else 0.0
        else:
            moyenne = ecart = ic95 = None
        agregats.append(
            {
                "scenario": scenario,
                "n": int(n),
                "panne": int(panne),
                "nb_essais": len(essais),
                "latence_moy_ms": None if moyenne is None else round(moyenne, 1),
                "latence_sd_ms": None if not latences else round(ecart, 1),
                "latence_ic95_ms": None if not latences else round(ic95, 1),
                "p95_ms": None if not p95 else round(statistics.mean(p95), 1),
                "debit_moy_tx_s": None if not debits else round(statistics.mean(debits), 2),
                "debit_sd_tx_s": None if len(debits) < 2 else round(statistics.stdev(debits), 2),
                "tx_ok": tx_ok,
                "tx_total": tx_total,
                "statut": "bloque" if bloque else "operationnel",
            }
        )
    return agregats


def ecrire_agregats(agregats: list[dict[str, object]]) -> None:
    champs = [
        "scenario",
        "n",
        "panne",
        "nb_essais",
        "latence_moy_ms",
        "latence_sd_ms",
        "latence_ic95_ms",
        "p95_ms",
        "debit_moy_tx_s",
        "debit_sd_tx_s",
        "tx_ok",
        "tx_total",
        "statut",
    ]
    with (RESULTATS / "mesures_agregees.csv").open("w", newline="", encoding="utf-8") as flux:
        writer = csv.DictWriter(flux, fieldnames=champs)
        writer.writeheader()
        writer.writerows(agregats)


def etiquettes(agregats: list[dict[str, object]]) -> list[str]:
    noms = {
        ("S1", 4, 0): "S1\nn=4\nsans retard",
        ("S2", 4, 0): "S2\nn=4\nretard",
        ("S3", 7, 0): "S3\nn=7",
        ("S3", 10, 0): "S3\nn=10",
        ("S4", 4, 1): "S4\nn=4\nf=1",
        ("S4", 4, 2): "S4\nn=4\nf+1",
    }
    return [noms.get((str(a["scenario"]), int(a["n"]), int(a["panne"])), f"{a['scenario']}\nn={a['n']}") for a in agregats]


def sauver(fig: plt.Figure, nom: str) -> None:
    for extension in ("pdf", "png"):
        fig.savefig(FIGURES / f"{nom}.{extension}", bbox_inches="tight")
    plt.close(fig)


def figure_latence(agregats: list[dict[str, object]]) -> None:
    actifs = [a for a in agregats if a["statut"] == "operationnel"]
    libelles = etiquettes(actifs)
    moyennes = [float(a["latence_moy_ms"]) for a in actifs]
    ecarts = [float(a["latence_sd_ms"]) for a in actifs]
    p95 = [float(a["p95_ms"]) for a in actifs]
    positions = list(range(len(actifs)))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.85), constrained_layout=True)
    couleurs = [BLEU, BLEU, VERT, VERT, ROUGE]
    ax1.bar(positions, moyennes, yerr=ecarts, capsize=3, color=couleurs[: len(actifs)], width=0.62)
    ax1.axhline(2000, color=GRIS, ls="--", lw=0.8)
    ax1.text(len(actifs) - 0.5, 2040, "seuil de confort 2 s", ha="right", fontsize=7, color=GRIS)
    ax1.set_xticks(positions)
    ax1.set_xticklabels(libelles)
    ax1.set_ylabel("latence moyenne (ms)")
    ax1.set_ylim(0, 3100)
    ax1.grid(axis="y", alpha=0.25)
    ax1.set_title("(a) Latence moyenne, ecart-type")

    ax2.bar(positions, p95, color=couleurs[: len(actifs)], width=0.62)
    ax2.axhline(2000, color=GRIS, ls="--", lw=0.8)
    ax2.set_xticks(positions)
    ax2.set_xticklabels(libelles)
    ax2.set_ylabel("95e centile (ms)")
    ax2.set_ylim(0, 6500)
    ax2.grid(axis="y", alpha=0.25)
    ax2.set_title("(b) Queue de latence, p95")
    sauver(fig, "fig3_latence")


def figure_debit(agregats: list[dict[str, object]]) -> None:
    libelles = etiquettes(agregats)
    debits = [float(a["debit_moy_tx_s"] or 0.0) for a in agregats]
    ecarts = [float(a["debit_sd_tx_s"] or 0.0) for a in agregats]
    positions = list(range(len(agregats)))
    couleurs = [BLEU, BLEU, VERT, VERT, ROUGE, ROUGE]

    fig, ax = plt.subplots(figsize=(3.5, 2.65), constrained_layout=True)
    barres = ax.bar(
        positions,
        debits,
        yerr=ecarts,
        capsize=3,
        color=couleurs[: len(agregats)],
        width=0.62,
    )
    barres[-1].set_hatch("//")
    barres[-1].set_edgecolor("white")
    ax.axhline(1.0, color=GRIS, ls="--", lw=0.8)
    ax.text(len(agregats) - 0.5, 1.3, "1 tx/s", ha="right", fontsize=7, color=GRIS)
    for position, valeur in zip(positions, debits):
        ax.text(position, valeur + 0.45, f"{valeur:.1f}", ha="center", fontsize=7)
    ax.set_xticks(positions)
    ax.set_xticklabels(libelles)
    ax.set_ylabel("debit (tx/s)")
    ax.set_ylim(0, 18)
    ax.grid(axis="y", alpha=0.25)
    ax.set_title("Debit selon le scenario")
    sauver(fig, "fig4_debit")


def figure_timeline() -> None:
    with (RESULTATS / "timeline_pannes.csv").open(encoding="utf-8") as flux:
        lignes = list(csv.DictReader(flux))
    temps = [float(ligne["t_s"]) for ligne in lignes]
    hauteurs = [int(ligne["hauteur"]) for ligne in lignes]
    phases = [ligne["phase"] for ligne in lignes]

    fig, ax = plt.subplots(figsize=(7.2, 2.8), constrained_layout=True)
    debut = 0
    couleur = {
        "nominal": "#dbe5f1",
        "f-1 panne": "#fff2cc",
        "f+1 pannes": "#f4cccc",
        "reprise": "#d9ead3",
    }
    for i in range(1, len(phases) + 1):
        if i == len(phases) or phases[i] != phases[debut]:
            ax.axvspan(temps[debut], temps[i - 1], color=couleur.get(phases[debut], "#eeeeee"), alpha=0.75, lw=0)
            ax.text(
                (temps[debut] + temps[i - 1]) / 2,
                min(hauteurs) - 1.5,
                phases[debut],
                ha="center",
                va="top",
                fontsize=7,
                color=GRIS,
            )
            debut = i
    ax.step(temps, hauteurs, where="post", color=BLEU, lw=2)
    for x in (temps[0], temps[-1]):
        ax.axvline(x, color=GRIS, lw=0.6, ls=":")
    ax.set_ylim(min(hauteurs) - 7, max(hauteurs) + 2)
    ax.set_xlabel("temps (s)")
    ax.set_ylabel("hauteur de bloc")
    ax.set_title("Progression de la chaine pendant les pannes (n = 4)")
    ax.grid(alpha=0.25)
    ax.annotate(
        "f + 1 panne : hauteur constante",
        xy=(35, 39059),
        xytext=(22, 39046),
        fontsize=7,
        color=ROUGE,
        arrowprops=dict(arrowstyle="->", color=ROUGE, lw=0.9),
    )
    ax.annotate(
        "reprise apres redemarrage",
        xy=(43, 39060),
        xytext=(46, 39046),
        fontsize=7,
        color=VERT,
        arrowprops=dict(arrowstyle="->", color=VERT, lw=0.9),
    )
    sauver(fig, "fig5_pannes")


def tableau_markdown(agregats: list[dict[str, object]]) -> None:
    lignes = [
        "# Tableau agrege des mesures",
        "",
        "| Scenario | n | Pannes | Essais | Latence moy. (ms) | IC95 (ms) | p95 (ms) | Debit (tx/s) | Statut |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for a in agregats:
        latence = "—" if a["latence_moy_ms"] is None else f"{a['latence_moy_ms']}"
        ic = "—" if a["latence_ic95_ms"] is None else f"±{a['latence_ic95_ms']}"
        p95 = "—" if a["p95_ms"] is None else f"{a['p95_ms']}"
        debit = "0,0" if a["debit_moy_tx_s"] is None else f"{a['debit_moy_tx_s']}".replace(".", ",")
        lignes.append(
            f"| {a['scenario']} | {a['n']} | {a['panne']} | {a['nb_essais']} | {latence.replace('.', ',')} | {ic.replace('.', ',')} | {p95.replace('.', ',')} | {debit} | {a['statut']} |"
        )
    (RESULTATS / "tableau_resultats.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")


def main() -> None:
    mesures = charger_mesures()
    agregats = agreger(mesures)
    ecrire_agregats(agregats)
    tableau_markdown(agregats)
    figure_latence(agregats)
    figure_debit(agregats)
    figure_timeline()
    print("Figures 3, 4 et 5 ecrites dans resultats/figures/")


if __name__ == "__main__":
    main()
