#!/usr/bin/env python3
"""Analyse theorique du consensus BFT et figures 1, 2 et 6.

Le script ne depend que de la bibliotheque standard et de matplotlib.
Il lit donnees/latences_villes.csv, ecrit resultats/analyse_theorique.csv
et produit les figures dans resultats/figures/.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

RACINE = Path(__file__).resolve().parents[1]
DONNEES = RACINE / "donnees"
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
        "xtick.labelsize": 8,
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


def charger_latences() -> list[dict[str, str]]:
    with (DONNEES / "latences_villes.csv").open(encoding="utf-8") as flux:
        return list(csv.DictReader(flux))


def parametres(n: int) -> dict[str, int]:
    f = (n - 1) // 3
    quorum = 2 * f + 1
    return {
        "n": n,
        "f": f,
        "quorum": quorum,
        "intersection": max(0, 2 * quorum - n),
        "marge": n - (3 * f + 1),
        "messages": 2 * n * n - n,
    }


def ecrire_analyse() -> list[dict[str, int]]:
    lignes = [parametres(n) for n in range(4, 21)]
    with (RESULTATS / "analyse_theorique.csv").open("w", newline="", encoding="utf-8") as flux:
        champs = ["n", "f", "quorum", "intersection", "marge", "messages"]
        writer = csv.DictWriter(flux, fieldnames=champs)
        writer.writeheader()
        writer.writerows(lignes)
    return lignes


def sauver(fig: plt.Figure, nom: str) -> None:
    for extension in ("pdf", "png"):
        fig.savefig(FIGURES / f"{nom}.{extension}", bbox_inches="tight")
    plt.close(fig)


def figure_quorums() -> None:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 2.75), constrained_layout=True)

    ax1.set_xlim(-0.6, 3.6)
    ax1.set_ylim(-1.15, 1.15)
    ax1.axis("off")
    for i in range(4):
        ax1.scatter([i], [0], s=180, color=BLEU, zorder=3)
        ax1.text(i, -0.22, f"n{i}", ha="center", va="top", fontsize=8)
    ax1.plot([0, 2], [0.42, 0.42], color=VERT, lw=3, solid_capstyle="round")
    ax1.plot([1, 3], [-0.42, -0.42], color=ORANGE, lw=3, solid_capstyle="round")
    ax1.text(1.0, 0.58, "Q1 = {n0, n1, n2}", ha="center", color=VERT, fontsize=8)
    ax1.text(2.0, -0.68, "Q2 = {n1, n2, n3}", ha="center", color=ORANGE, fontsize=8)
    for i in (1, 2):
        ax1.add_patch(plt.Circle((i, 0), 0.25, fill=False, color=ROUGE, lw=1.5, zorder=2))
    ax1.text(1.5, 0.02, "∩ ≥ f + 1", ha="center", va="center", color=ROUGE, fontsize=8, fontweight="bold")
    ax1.set_title("(a) Deux quorums se recoupent (n = 4, f = 1)")

    configurations = [parametres(4), parametres(7), parametres(10)]
    positions = range(len(configurations))
    largeur = 0.2
    series = [
        ("n", "validateurs n", BLEU),
        ("quorum", "quorum 2f + 1", VERT),
        ("f", "fautes tolerees f", ORANGE),
        ("intersection", "intersection f + 1", ROUGE),
    ]
    for decalage, (cle, etiquette, couleur) in enumerate(series):
        valeurs = [c[cle] for c in configurations]
        ax2.bar(
            [p + (decalage - 1.5) * largeur for p in positions],
            valeurs,
            width=largeur,
            label=etiquette,
            color=couleur,
        )
    ax2.set_xticks(list(positions))
    ax2.set_xticklabels([f"n = {c['n']}" for c in configurations])
    ax2.set_ylabel("nombre de noeuds")
    ax2.set_ylim(0, 11.5)
    ax2.legend(ncol=2, frameon=False, loc="upper left")
    ax2.set_title("(b) Tailles pour les configurations mesurees")
    ax2.grid(axis="y", alpha=0.25)

    sauver(fig, "fig1_quorums")


def figure_phases() -> None:
    fig, ax = plt.subplots(figsize=(7.2, 3.4), constrained_layout=True)
    participants = [
        (0.4, "Client"),
        (2.0, "Primaire"),
        (3.5, "Replique 1"),
        (5.0, "Replique 2"),
        (6.5, "Replique 3"),
    ]
    for x, nom in participants:
        ax.plot([x, x], [0.25, 5.35], color=GRIS, lw=0.8, ls=(0, (2, 3)), zorder=1)
        ax.text(x, 5.55, nom, ha="center", va="bottom", fontsize=8)

    def fleche(x1: float, x2: float, y: float, texte: str, couleur: str) -> None:
        ax.add_patch(
            FancyArrowPatch(
                (x1, y),
                (x2, y),
                arrowstyle="-|>",
                mutation_scale=9,
                lw=1.0,
                color=couleur,
                shrinkA=2,
                shrinkB=2,
                zorder=2,
            )
        )
        ax.text((x1 + x2) / 2, y + 0.11, texte, ha="center", va="bottom", fontsize=6.5, color=couleur)

    fleche(0.4, 2.0, 5.0, "REQUEST", GRIS)
    for x in (3.5, 5.0, 6.5):
        fleche(2.0, x, 4.25, "PRE-PREPARE", BLEU)
    for indice, depart in enumerate((3.5, 5.0, 6.5)):
        for arrivee in (2.0, 3.5, 5.0, 6.5):
            if arrivee != depart:
                fleche(depart, arrivee, 3.42 - 0.05 * indice, "", VERT)
    ax.text(4.95, 3.62, "PREPARE : diffusion a tous", ha="center", color=VERT, fontsize=7)
    for indice, depart in enumerate((3.5, 5.0, 6.5)):
        for arrivee in (2.0, 3.5, 5.0, 6.5):
            if arrivee != depart:
                fleche(depart, arrivee, 2.52 - 0.05 * indice, "", ORANGE)
    ax.text(4.95, 2.72, "COMMIT : diffusion a tous", ha="center", color=ORANGE, fontsize=7)
    for x in (3.5, 5.0, 6.5):
        fleche(x, 0.4, 1.55, "REPLY", VERT)

    ax.set_xlim(-0.2, 7.1)
    ax.set_ylim(0.0, 5.9)
    ax.set_yticks([])
    ax.set_xticks([])
    for cote in ("top", "right", "left", "bottom"):
        ax.spines[cote].set_visible(False)
    ax.set_title("Sequence simplifiee de PBFT (n = 4, f = 1)")
    sauver(fig, "fig2_phases_pbft")


def figure_messages() -> None:
    valeurs = [parametres(n) for n in range(4, 21)]
    n = [v["n"] for v in valeurs]
    messages = [v["messages"] for v in valeurs]
    fig, ax = plt.subplots(figsize=(3.45, 2.55), constrained_layout=True)
    ax.plot(n, messages, color=BLEU, marker="o", ms=3, lw=1.5)
    for cible in (4, 7, 10):
        p = parametres(cible)
        ax.scatter([cible], [p["messages"]], color=ORANGE, zorder=3, s=22)
        ax.annotate(
            f"n = {cible}\n{p['messages']} msg",
            (cible, p["messages"]),
            textcoords="offset points",
            xytext=(5, 8 if cible < 10 else -16),
            fontsize=7,
            color=GRIS,
        )
    ax.set_xlabel("nombre de validateurs n")
    ax.set_ylabel("messages par decision")
    ax.set_title("Croissance en O(n^2) des messages")
    ax.grid(alpha=0.25)
    sauver(fig, "fig6_messages")


def resume_latences() -> None:
    lignes = charger_latences()
    retards = [float(ligne["retard_aller_ms"]) for ligne in lignes]
    with (RESULTATS / "resume_latences.csv").open("w", newline="", encoding="utf-8") as flux:
        writer = csv.writer(flux)
        writer.writerow(["nb_villes", "retard_min_ms", "retard_max_ms", "retard_moyen_ms"])
        writer.writerow([len(retards), min(retards), max(retards), round(sum(retards) / len(retards), 1)])


def main() -> None:
    ecrire_analyse()
    resume_latences()
    figure_quorums()
    figure_phases()
    figure_messages()
    print("Figures 1, 2 et 6 ecrites dans resultats/figures/")


if __name__ == "__main__":
    main()
