# A9 — Consensus BFT pour un consortium universitaire

Dépôt du **groupe 3** pour le module *Cryptographie & Technologies Blockchain*
(Pr Gervais Mendy, ESP-UCAD / LITA).

Le sujet étudie la tenue d'un registre de diplômes par plusieurs universités de
l'UEMOA, sans tiers de confiance unique. Chaque université exploite un validateur
CometBFT ; les empreintes des diplômes sont inscrites dans un registre répliqué
et les autres universités peuvent les vérifier. La question posée est celle de la
sécurité, de la cohérence et des performances d'un consensus BFT lorsque des
validateurs tombent en panne ou se comportent de façon byzantine.

## Contenu du dépôt

Le dossier `animation/commun/` est fourni par le cours : il ne doit pas être
modifié. Le fichier `animation/theme_local.tex` ne sert que de secours si ce
thème n'est pas présent.

```text
GROUPE.md                         fiche du groupe, sujets et rôles
METHODOLOGIE.md                   méthode de travail et règles de preuve
EVALUATION.md                     grille d'évaluation et auto-évaluation
plan/plan.md                      plan d'une page (question, hypothèse, méthode)
bibliographie/references.bib      sources primaires et secondaires
animation/animation.tex           diapositives LaTeX (12 au plus)
animation/theme_local.tex         thème local de secours (ne remplace pas commun/)
animation/demonstration.md        scénario de démonstration et plan de secours
discussion/questions-discutant.md 2 questions critiques sur A14
synthese/synthese-rapporteur.md   synthèse d'une page du sujet A1
quiz/questions.md                 3 QCM avec réponses
article/article.tex               rapport-article au format IEEE
code/                             simulation, mesures, figures, tests
donnees/                          latences, scénarios, fiche des données
resultats/                        mesures brutes, agrégées et figures
outils/verifier_depot.py          contrôle avant dépôt
.github/workflows/ci.yml          compilation et vérifications automatiques
```

## Régénérer les figures et les tableaux

Toutes les figures de l'article sont régénérées par :

```bash
bash code/reproduire.sh
```

Le script utilise `python3` si `matplotlib` est disponible. Sinon, il crée un
environnement `.venv` et installe `code/requirements.txt`. Les figures sont
écrites dans `resultats/figures/` en PDF et PNG, et les tableaux agrégés dans
`resultats/`.

Les figures sont produites à partir de :

- `resultats/mesures_brutes.csv` : mesures CometBFT réelles (3 essais par scénario) ;
- `resultats/timeline_pannes.csv` : chronologie réelle des hauteurs de bloc pendant
  l'arrêt de validateurs ;
- `donnees/latences_villes.csv` : retards aller simple injectés par `tc netem` ;
- `donnees/scenarios.csv` : définition des scénarios S1 à S4.

## Relancer l'expérience CometBFT (optionnel)

Le script `code/experimenter.sh` reconstruit un réseau de test Docker et rejoue
les scénarios. Il faut Docker, les images `cometbft/cometbft:v0.38.17` et
`nicolaka/netshoot`, et environ 8 Go de RAM. Les clés privées du réseau de test
ne doivent **jamais** être poussées : `testnet/` est exclu par `.gitignore`.

```bash
bash code/experimenter.sh 4    # crée et lance 4 validateurs
bash code/experimenter.sh 7
bash code/experimenter.sh 10
```

## Compiler les documents

Avec une distribution LaTeX contenant `IEEEtran`, `beamer` et `babel-french` :

```bash
latexmk -cd -pdf article/article.tex
latexmk -cd -pdf animation/animation.tex
```

Sans `latexmk` :

```bash
cd article && pdflatex article.tex && bibtex article && pdflatex article.tex && pdflatex article.tex
cd ../animation && pdflatex animation.tex && pdflatex animation.tex
```

## Vérifier avant de déposer

```bash
python3 outils/verifier_depot.py --etape rendu-article
python3 -m unittest discover -s code/tests -v
```

## Jalons et étiquettes Git

```bash
git add -A
git commit -m "Plan d'une page"
git push
git tag j-14-plan
git push origin j-14-plan
```

Ordre des étiquettes : `j-14-plan`, `j-7-biblio`, `j-3-depot`, `j2-corrige`,
`etat-art`, `resultats-prelim`, `rendu-article`, `version-soumission`.

En cas d'échec d'un contrôle, corriger puis reposer l'étiquette :

```bash
git tag -d j-3-depot
git push origin :refs/tags/j-3-depot
git tag j-3-depot
git push origin j-3-depot
```

## Règles et éthique

- Aucune attaque contre un système réel. Le banc est un réseau de test local,
  avec des données synthétiques.
- Aucun secret, aucune clé privée, aucun jeton dans le dépôt. `testnet/`, `.env`
  et `.venv/` sont ignorés.
- Toutes les sources sont citées dans `bibliographie/references.bib`.
- L'usage d'un outil d'IA générative est déclaré dans `GROUPE.md`, dans l'article
  et ci-dessous.

## Déclaration d'usage de l'IA

Un outil d'IA générative a été utilisé pour aider à structurer le dépôt, à mettre
en forme le LaTeX et à relire le français. Les mesures, les choix de protocole,
les sources et l'interprétation ont été vérifiés par les trois membres du groupe.
