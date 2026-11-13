# Méthodologie du groupe 3

Ce document décrit la démarche suivie pour le sujet A9, les règles de preuve et
les précautions prises avant chaque dépôt. Il est à lire avant J-14.

## 1. Question, hypothèse et critère de réfutation

La question de recherche est : *dans quelle mesure un protocole de consensus BFT
garantit-il la sécurité et la cohérence des transactions tout en maintenant des
performances acceptables dans un consortium universitaire soumis à des
comportements byzantins ?*

L'hypothèse est double :

1. **Sûreté :** tant que moins d'un tiers des validateurs est fautif, les
   validateurs honnêtes ne divergent pas.
2. **Performance :** la latence de finalisation et le débit se dégradent lorsque
   le nombre de validateurs et les perturbations réseau augmentent, mais restent
   compatibles avec la vérification de diplômes.

Le critère de réfutation de la partie performance est explicite : si, à
configuration égale et avec un délai entre blocs réduit, le temps de consensus
ne croît pas de façon significative entre 4 et 10 validateurs, alors l'hypothèse
« les performances se dégradent » est fausse à cette échelle. Nous ne prétendons
pas réfuter la partie sûreté : elle est établie par le modèle et vérifiée par la
littérature, puis confrontée à des pannes franches dans notre banc.

## 2. Ce que nous mesurons et ce que nous ne mesurons pas

### Mesuré

- Latence de finalisation : temps entre l'envoi d'une transaction et la réponse
  `broadcast_tx_commit` de CometBFT.
- Débit : nombre de transactions validées par seconde, avec 20 envois simultanés
  et 200 transactions par essai pour S1–S3, 50 pour S4.
- Comportement en panne : arrêt de `f` puis `f + 1` validateurs sur 4, avec suivi
  de la hauteur de bloc toutes les 0,5 s.
- Temps de reprise après redémarrage des validateurs.
- Nombre de messages par décision : calcul analytique PBFT, `2n² − n`.

### Non mesuré, et assumé comme tel

- Un validateur qui **ment activement** (double vote, messages contradictoires).
  Le banc ne provoque que des pannes franches (`docker stop`). La garantie
  byzantine est argumentée par la théorie et par l'intersection des quorums.
- Le coût du consensus isolé du délai `timeout_commit` de 1 s. La latence
  observée est donc un majorant pratique, pas le temps de vote pur.
- La perte de paquets, les attaques réseau et les pannes électriques.
- Les performances sur plusieurs machines physiques : les validateurs partagent
  le même processeur.

## 3. Choix du protocole et de l'outil

Le cours présente PBFT, Tendermint/CometBFT et HotStuff. Nous retenons
CometBFT v0.38.17 pour trois raisons :

- il implémente un consensus BFT de type Tendermint, avec finalité immédiate ;
- il est disponible en image Docker, donc reproductible sans compilation ;
- il expose une interface RPC simple et une application `kvstore` qui permet
  d'inscrire des diplômes sans écrire de contrat.

PBFT reste notre référence théorique pour les phases, les quorums et la
croissance en `O(n²)`. CometBFT est l'implémentation mesurée.

## 4. Topologie et latences

Chaque nœud représente une université. Les retards aller simple injectés avec
`tc netem` sont des ordres de grandeur inspirés des distances régionales :

| Nœud | Université fictive | Ville | Retard aller simple |
|---|---|---|---:|
| node0 | UCAD | Dakar | 10 ms |
| node1 | UGB | Saint-Louis | 15 ms |
| node2 | Université Ki-Zerbo | Ouagadougou | 40 ms |
| node3 | Université Houphouët-Boigny | Abidjan | 35 ms |
| node4 | Université de Bamako | Bamako | 40 ms |
| node5 | Université de Niamey | Niamey | 45 ms |
| node6 | Université de Lomé | Lomé | 35 ms |
| node7 | Université de Cotonou | Cotonou | 35 ms |
| node8 | Université de Bissau | Bissau | 20 ms |
| node9 | Université de Ziguinchor | Ziguinchor | 15 ms |

Ces valeurs ne sont pas présentées comme des mesures de terrain. Elles servent à
tester la sensibilité du consensus à des délais de quelques dizaines de
millisecondes. Une version ultérieure devrait mesurer une matrice de latences
entre capitales avec `ping` ou des sondes publiques (RIPE Atlas) et l'injecter
par paire de nœuds.

## 5. Protocole expérimental

Pour chaque scénario, nous faisons **3 essais indépendants**. Pour S1–S3, chaque
essai comprend :

1. 20 transactions séquentielles pour la latence ;
2. 200 transactions avec 20 envois simultanés pour le débit ;
3. le calcul de la moyenne, de la médiane et du 95ᵉ centile des latences ;
4. la vérification qu'aucune transaction n'a échoué.

Pour S4, l'essai réduit la charge à 10 transactions séquentielles et 50
transactions en débit, afin de laisser la place aux arrêts et au redémarrage.

Les scénarios sont :

- **S1** : 4 validateurs, sans retard ajouté (référence).
- **S2** : 4 validateurs, avec les retards du tableau.
- **S3** : 7 puis 10 validateurs, avec retards.
- **S4** : 4 validateurs, arrêt de `f = 1` puis de `f + 1 = 2` validateurs,
  puis redémarrage.

Les fichiers `code/mesure.py`, `code/latence.sh`, `code/gen_compose.py` et
`code/experimenter.sh` permettent de rejouer les scénarios.

## 6. Règles de preuve et de citation

- Une affirmation sur un protocole est appuyée soit par une source primaire, soit
  par une mesure du dépôt, soit par un calcul explicite.
- Les résultats mesurés ne sont jamais présentés comme des résultats byzantins :
  le texte distingue systématiquement **pannes franches mesurées** et
  **tolérance byzantine argumentée**.
- Les références sont vérifiées dans `bibliographie/references.bib`. Au moins
  cinq sources primaires sont présentes.
- Les chiffres de la presse (Dakaractu, NDARINFO) sont signalés comme
  journalistiques et à recouper avec une source officielle.
- Toute figure de l'article est régénérée par `bash code/reproduire.sh` à partir
  des fichiers de `donnees/` et `resultats/`.

## 7. Éthique et sécurité

- Aucun système réel n'est attaqué : le banc est local, les universités sont
  fictives, les diplômes sont synthétiques.
- Aucune clé privée de validateur n'est publiée. Le dossier `testnet/` est dans
  `.gitignore`.
- Aucun secret, jeton ou mot de passe n'est présent dans le dépôt. Le script
  `outils/verifier_depot.py` vérifie ce point.
- Les données personnelles sont absentes : les transactions sont des chaînes
  `diplome-<identifiant aléatoire>=valide`.
- L'usage d'un outil d'IA générative est déclaré et limité à l'aide à la
  rédaction et à la mise en forme.

## 8. Organisation du travail

| Période | Travail |
|---|---|
| S1–S2 | lecture des chapitres 4 à 7, choix du sujet, fiche GROUPE.md |
| J-14 | plan d'une page, question et hypothèse |
| J-7 | cinq sources primaires, première version de l'état de l'art |
| J-3 | diapositives, questions pour A14, dépôt `j-3-depot` |
| Séance S4 | exposé A9, réponses aux discutants |
| J+2 | quiz, synthèse rapporteur A1, corrections `j2-corrige` |
| S5–S6 | expériences, résultats préliminaires, article |
| S6 + 5 jours | article final, figures régénérées, `rendu-article` |

## 9. Risques et parades

| Risque | Parade |
|---|---|
| Docker ou `tc netem` indisponible | résultats déjà mesurés dans `resultats/`, figures régénérées sans Docker |
| Machine trop faible pour 10 nœuds | mesure réelle faite avec 10 nœuds ; sinon réduire à 7 et le signaler |
| Confusion entre panne et faute byzantine | section dédiée, vocabulaire contrôlé, limite répétée dans l'article |
| Dérive du périmètre vers la véracité des diplômes | rappel : le consensus garantit l'accord, pas la vérité des données |
| Retard de dépôt | jalons et étiquettes listés dans le README, vérification automatique |
