# Quiz — A9 Consensus BFT pour un consortium universitaire

**Consigne :** une seule bonne réponse par question. Réponses et explications en
fin de document, à ne pas lire avant d'avoir répondu.

## Question 1 — Le seuil de tolérance

Un consortium réunit `n = 7` universités qui exécutent un consensus BFT
partiel-synchrone. Combien de validateurs peuvent être fautifs au maximum pour
que la sûreté et la vivacité soient garanties, dans le modèle classique
`n ≥ 3f + 1` ?

- A. 1 validateur
- B. 2 validateurs
- C. 3 validateurs
- D. 4 validateurs

## Question 2 — Les phases de PBFT

Dans PBFT, quel est l'ordre correct des phases après la requête du client ?

- A. Pre-prepare → prepare → commit → reply
- B. Prepare → pre-prepare → commit → reply
- C. Commit → prepare → pre-prepare → reply
- D. Pre-prepare → commit → prepare → reply

## Question 3 — Lire nos mesures

Dans notre banc CometBFT à 4 validateurs, nous arrêtons 2 validateurs
(`f + 1 = 2`). Que se passe-t-il, et pourquoi ?

- A. La chaîne continue avec une latence plus élevée, car il reste 2 nœuds.
- B. La chaîne se bifurque en deux branches, chacune avec 2 nœuds.
- C. La chaîne se bloque : il manque un quorum de `2f + 1 = 3` validateurs pour
  produire un bloc.
- D. La chaîne continue mais les transactions sont seulement ralenties, car le
  quorum est de `f + 1 = 2`.

---

## Réponses et explications

### Question 1 — Réponse B (2 validateurs)

Avec `n = 7`, la contrainte `n ≥ 3f + 1` donne `7 ≥ 3f + 1`, donc `f ≤ 2`.
Le quorum est `2f + 1 = 5` validateurs. Deux quorums de 5 parmi 7 se recoupent
en au moins `2 × 5 − 7 = 3 = f + 1` validateurs, dont au moins un est honnête.
C'est l'intersection qui empêche deux décisions contradictoires. Avec 3 fautifs,
le quorum de 5 pourrait être entièrement fautif ou deux quorums pourraient ne
plus se recouper sur un honnête.

**Source :** Lamport, Shostak et Pease (1982) ; Castro et Liskov (1999) ;
section IV de l'article.

### Question 2 — Réponse A

PBFT suit `pre-prepare`, `prepare`, `commit`, puis `reply`. Le primaire diffuse
le `pre-prepare` ; chaque réplique diffuse un `prepare` ; après avoir reçu
`2f` messages `prepare` compatibles, elle diffuse un `commit` ; après `2f + 1`
`commit`, elle exécute et répond au client. L'ordre `commit` avant `prepare`
n'a pas de sens dans PBFT.

**Source :** Castro et Liskov (1999) ; figure 2 de l'article.

### Question 3 — Réponse C

Avec `n = 4` et `f = 1`, le quorum est `2f + 1 = 3`. En arrêtant 2 nœuds, il ne
reste que 2 validateurs honnêtes, donc aucun quorum de 3 ne peut se former. La
chaîne se bloque : la hauteur reste constante et les transactions échouent. Ce
n'est pas une bifurcation (la sûreté tient), c'est une perte de vivacité. C'est
exactement ce que montre `fig5_pannes.pdf` : la hauteur plafonne pendant la
panne `f + 1`, puis reprend après redémarrage.

**Source :** nos mesures S4 (`resultats/timeline_pannes.csv`) ; section VI de
l'article.
