#!/usr/bin/env python3
"""Verificateur de depot pour le sujet A9 du groupe 3.

Usage :
    python3 outils/verifier_depot.py
    python3 outils/verifier_depot.py --etape j-3-depot
    python3 outils/verifier_depot.py --etape rendu-article --verbeux

Le script ne modifie aucun fichier. Il renvoie 0 si tout est conforme, 1 sinon.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]

ETAPES = {
    "j-14-plan": ["GROUPE.md", "plan/plan.md", "METHODOLOGIE.md"],
    "j-7-biblio": [
        "GROUPE.md",
        "plan/plan.md",
        "METHODOLOGIE.md",
        "bibliographie/references.bib",
    ],
    "j-3-depot": [
        "GROUPE.md",
        "plan/plan.md",
        "bibliographie/references.bib",
        "animation/animation.tex",
        "discussion/questions-discutant.md",
        "code/reproduire.sh",
        "METHODOLOGIE.md",
        "EVALUATION.md",
        "README.md",
    ],
    "j2-corrige": [
        "quiz/questions.md",
        "synthese/synthese-rapporteur.md",
        "animation/animation.tex",
    ],
    "etat-art": ["article/article.tex", "bibliographie/references.bib"],
    "resultats-prelim": [
        "article/article.tex",
        "resultats/mesures_brutes.csv",
        "resultats/mesures_agregees.csv",
        "resultats/figures/fig3_latence.pdf",
        "resultats/figures/fig4_debit.pdf",
        "resultats/figures/fig5_pannes.pdf",
    ],
    "rendu-article": [
        "GROUPE.md",
        "plan/plan.md",
        "bibliographie/references.bib",
        "animation/animation.tex",
        "discussion/questions-discutant.md",
        "synthese/synthese-rapporteur.md",
        "quiz/questions.md",
        "article/article.tex",
        "code/reproduire.sh",
        "METHODOLOGIE.md",
        "EVALUATION.md",
        "README.md",
        "outils/verifier_depot.py",
        "resultats/mesures_brutes.csv",
        "resultats/mesures_agregees.csv",
        "resultats/timeline_pannes.csv",
    ],
    "version-soumission": [
        "GROUPE.md",
        "plan/plan.md",
        "bibliographie/references.bib",
        "animation/animation.tex",
        "discussion/questions-discutant.md",
        "synthese/synthese-rapporteur.md",
        "quiz/questions.md",
        "article/article.tex",
        "code/reproduire.sh",
        "METHODOLOGIE.md",
        "EVALUATION.md",
        "README.md",
        "outils/verifier_depot.py",
        "resultats/mesures_brutes.csv",
        "resultats/mesures_agregees.csv",
        "resultats/timeline_pannes.csv",
        "resultats/figures/fig1_quorums.pdf",
        "resultats/figures/fig2_phases_pbft.pdf",
        "resultats/figures/fig3_latence.pdf",
        "resultats/figures/fig4_debit.pdf",
        "resultats/figures/fig5_pannes.pdf",
        "resultats/figures/fig6_messages.pdf",
    ],
}

FIGURES_ATTENDUES = [
    "fig1_quorums.pdf",
    "fig2_phases_pbft.pdf",
    "fig3_latence.pdf",
    "fig4_debit.pdf",
    "fig5_pannes.pdf",
    "fig6_messages.pdf",
]

TEXTES = {".md", ".tex", ".py", ".sh", ".csv", ".yml", ".yaml", ".bib", ".txt", ".json"}


class Verification:
    def __init__(self, verbeux: bool = False) -> None:
        self.verbeux = verbeux
        self.erreurs: list[str] = []
        self.avertissements: list[str] = []

    def ok(self, message: str) -> None:
        if self.verbeux:
            print(f"[OK]   {message}")

    def erreur(self, message: str) -> None:
        self.erreurs.append(message)
        print(f"[ERR]  {message}")

    def avertir(self, message: str) -> None:
        self.avertissements.append(message)
        print(f"[WARN] {message}")

    def fichier(self, chemin: str, taille_min: int = 20) -> None:
        cible = RACINE / chemin
        if not cible.is_file():
            self.erreur(f"fichier manquant : {chemin}")
        elif cible.stat().st_size < taille_min:
            self.erreur(f"fichier trop petit : {chemin} ({cible.stat().st_size} octets)")
        else:
            self.ok(f"fichier present : {chemin}")


def lire(chemin: str) -> str:
    return (RACINE / chemin).read_text(encoding="utf-8", errors="replace")


def verifier_contenu(v: Verification) -> None:
    article = RACINE / "article/article.tex"
    if article.is_file():
        texte = lire("article/article.tex")
        for attendu in ("\\documentclass", "\\begin{document}", "\\end{document}", "\\bibliography"):
            if attendu not in texte:
                v.erreur(f"article/article.tex ne contient pas {attendu!r}")
        if "\\section{Introduction}" not in texte:
            v.erreur("article/article.tex : section Introduction absente")
        if "État de l'art" not in texte and "etat de l'art" not in texte:
            v.avertir("article/article.tex : section état de l'art a verifier")
        v.ok("structure LaTeX de l'article verifiee")

    animation = RACINE / "animation/animation.tex"
    if animation.is_file():
        texte = lire("animation/animation.tex")
        frames = len(re.findall(r"\\begin\{frame\}", texte))
        if frames == 0:
            v.erreur("animation/animation.tex : aucune diapositive")
        elif frames > 12:
            v.erreur(f"animation/animation.tex : {frames} diapositives (maximum 12)")
        else:
            v.ok(f"animation : {frames} diapositives (<= 12)")

    bib = RACINE / "bibliographie/references.bib"
    if bib.is_file():
        entrees = re.findall(r"@\w+\s*\{", lire("bibliographie/references.bib"))
        if len(entrees) < 5:
            v.erreur(f"bibliographie : {len(entrees)} entrees (minimum 5)")
        else:
            v.ok(f"bibliographie : {len(entrees)} entrees")

    quiz = RACINE / "quiz/questions.md"
    if quiz.is_file():
        texte = lire("quiz/questions.md")
        questions = len(re.findall(r"^## Question", texte, flags=re.MULTILINE))
        if questions < 3:
            v.erreur(f"quiz : {questions} questions (minimum 3)")
        if "Réponses" not in texte:
            v.erreur("quiz : section de reponses absente")
        v.ok(f"quiz : {questions} questions")

    discussion = RACINE / "discussion/questions-discutant.md"
    if discussion.is_file():
        texte = lire("discussion/questions-discutant.md")
        questions = len(re.findall(r"^## Question", texte, flags=re.MULTILINE))
        if questions < 2:
            v.erreur(f"discussion : {questions} questions (minimum 2)")
        else:
            v.ok(f"discussion : {questions} questions")

    synthese = RACINE / "synthese/synthese-rapporteur.md"
    if synthese.is_file():
        mots = len(re.findall(r"\b\w+\b", lire("synthese/synthese-rapporteur.md")))
        if mots < 300:
            v.avertir(f"synthese : {mots} mots, sans doute trop courte pour une page")
        elif mots > 1000:
            v.avertir(f"synthese : {mots} mots, sans doute plus d'une page")
        else:
            v.ok(f"synthese : {mots} mots")

    script = RACINE / "code/reproduire.sh"
    if script.is_file() and not (script.stat().st_mode & 0o111):
        v.erreur("code/reproduire.sh n'est pas executable (chmod +x)")


def verifier_figures(v: Verification) -> None:
    dossier = RACINE / "resultats/figures"
    for nom in FIGURES_ATTENDUES:
        cible = dossier / nom
        if not cible.is_file():
            v.erreur(f"figure manquante : resultats/figures/{nom}")
        elif cible.stat().st_size < 1000:
            v.erreur(f"figure trop petite : resultats/figures/{nom}")
        else:
            v.ok(f"figure presente : {nom}")

    article = RACINE / "article/article.tex"
    if article.is_file():
        texte = lire("article/article.tex")
        for reference in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", texte):
            nom = Path(reference).name
            if not (dossier / nom).is_file():
                v.erreur(f"figure referencee mais absente : {reference}")


def verifier_securite(v: Verification) -> None:
    motifs = [
        (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "cle privee PEM"),
        (re.compile(r"(?i)password\s*=\s*['\"][^'\"]+['\"]"), "mot de passe en clair"),
        (re.compile(r"(?i)api[_-]?key\s*=\s*['\"][^'\"]+['\"]"), "cle API en clair"),
        (re.compile(r"(?i)token\s*=\s*['\"][^'\"]{8,}['\"]"), "jeton en clair"),
    ]
    for chemin in RACINE.rglob("*"):
        if not chemin.is_file() or chemin.suffix.lower() not in TEXTES:
            continue
        if any(part in {".git", ".venv", "venv", "testnet", "__pycache__"} for part in chemin.parts):
            continue
        if chemin.stat().st_size > 1_000_000:
            continue
        try:
            texte = chemin.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for motif, etiquette in motifs:
            if motif.search(texte):
                v.erreur(f"secret potentiel ({etiquette}) dans {chemin.relative_to(RACINE)}")

    for chemin in RACINE.rglob("priv_validator_key.json"):
        v.erreur(f"cle de validation presente dans le depot : {chemin.relative_to(RACINE)}")
    for chemin in RACINE.rglob("*"):
        if chemin.is_file() and chemin.stat().st_size > 50 * 1024 * 1024:
            v.erreur(f"fichier de plus de 50 Mo : {chemin.relative_to(RACINE)}")
    v.ok("controle des secrets et des gros fichiers termine")


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument(
        "--etape",
        choices=sorted(ETAPES),
        default="rendu-article",
        help="jalon a verifier (defaut : rendu-article)",
    )
    parseur.add_argument("--verbeux", action="store_true", help="afficher aussi les controles reussis")
    parseur.add_argument("--liste", action="store_true", help="lister les jalons disponibles")
    arguments = parseur.parse_args()

    if arguments.liste:
        for etape in sorted(ETAPES):
            print(etape)
        return 0

    print(f"Verification du depot : {RACINE}")
    print(f"Jalon : {arguments.etape}\n")
    v = Verification(verbeux=arguments.verbeux)

    for chemin in ETAPES[arguments.etape]:
        v.fichier(chemin)
    verifier_contenu(v)
    verifier_figures(v)
    verifier_securite(v)

    print()
    if v.erreurs:
        print(f"ECHEC : {len(v.erreurs)} erreur(s), {len(v.avertissements)} avertissement(s).")
        return 1
    print(f"SUCCES : aucune erreur, {len(v.avertissements)} avertissement(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
