# Évaluation et auto-évaluation — groupe 3

## 1. Barème du rapport-article (25 % du module)

| Jalon | Points | Ce qui est vérifié | État |
|---|---:|---|---|
| `etat-art` | 3 | au moins 5 sources primaires, positionnement, question | fait |
| `resultats-prelim` | 3 | banc, scénarios, premières mesures, figures | fait |
| `article final` | 14 | fond, méthode, résultats, discussion, forme IEEE | fait |
| **Total** | **20** | | |

Un jalon en retard perd la moitié de ses points. Les points ci-dessus sont ceux
du rapport-article ; l'animation et la participation sont notées séparément
(25 % du module).

## 2. Grille détaillée de l'article

| Critère | Attendu | Preuve dans le dépôt |
|---|---|---|
| Problème et question | problème réel, question précise, hypothèse testable | `plan/plan.md`, section I |
| État de l'art | 5 sources primaires, une ligne d'apport et une limite par source | `article/article.tex` §III, `bibliographie/references.bib` |
| Mécanisme | PBFT, CometBFT, quorums, `n ≥ 3f + 1` | §IV, figures 1 et 2 |
| Méthode | outil, topologie, latences, charge, scénarios, métriques | §V, `donnees/`, `code/` |
| Résultats | tableaux, figures, incertitude, reproductibilité | §VI, `resultats/`, `code/reproduire.sh` |
| Discussion | limites, menaces à la validité, gouvernance | §VII |
| Forme | IEEE, 8 à 12 pages, français, références complètes | `article/article.tex` |
| Éthique | pas d'attaque réelle, pas de secret, IA déclarée | `METHODOLOGIE.md`, `README.md` |

## 3. Grille de l'animation et des rôles

| Élément | Attendu | Où |
|---|---|---|
| Diapositives | 12 au plus, claires, corrigées à J+2 | `animation/animation.tex` |
| Démonstration | réseau CometBFT, écriture puis preuve d'inclusion | `code/experimenter.sh`, `animation/demonstration.md` |
| Questions de discutant | 2 questions critiques sur A14, avec réponse attendue | `discussion/questions-discutant.md` |
| Synthèse de rapporteur | 1 page sur A1, fidèle et critique | `synthese/synthese-rapporteur.md` |
| Quiz | 3 QCM avec réponse et explication | `quiz/questions.md` |
| Participation | discussion croisée, respect du temps | fiche de rôle dans `GROUPE.md` |

## 4. Auto-évaluation du groupe

### Points forts

- Question de recherche reliée à un problème réel de l'UEMOA.
- Distinction rigoureuse entre panne franche, faute byzantine et véracité des
  données.
- Mesures réelles avec CometBFT, à 4, 7 et 10 validateurs, avec latence injectée.
- Toutes les figures sont régénérables sans Docker à partir des données du dépôt.
- Rôles de discutant et de rapporteur documentés.

### Points à renforcer

- Le banc ne teste pas un validateur qui ment activement (double vote). C'est la
  principale limite expérimentale, clairement annoncée.
- Les latences sont des ordres de grandeur, pas une matrice mesurée entre
  capitales.
- Le débit est borné par le client de mesure (20 envois simultanés), pas par la
  capacité maximale de CometBFT.
- Les validateurs partagent une seule machine.
- Le plan de secours de la démonstration doit être répété avant la séance.

### Note proposée

| Élément | Note /20 |
|---|---:|
| État de l'art | 16 |
| Résultats préliminaires | 17 |
| Article final | 17 |
| Animation | 16 |
| Rôles discutant / rapporteur | 17 |

## 5. Corrections demandées par les discutants (J+2)

- Remplacer « Groupe [n] » par « groupe 3 » et indiquer discutants et rapporteurs.
- Ajouter le scénario de secours et les résultats mesurés.
- Renuméroter les références et ajouter BLOCKBENCH.
- Préciser que 28, 91 et 190 messages sont un calcul PBFT d'ordre de grandeur.
- Passer de 16 à 12 diapositives.
- Développer les sigles à leur première utilisation : BFT, PBFT, ABCI, GST.
