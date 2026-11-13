# Plan d'une page — A9 Consensus BFT pour un consortium universitaire

**Groupe 3** : Souleymane Kone, Mouhamadou Makhtar Gueye, Fatou Kine Thioub
**Module** : Cryptographie & Technologies Blockchain — Pr Gervais Mendy, ESP-UCAD / LITA
**Séance** : S4, jeudi 12 novembre 2026 — **Jalon** : `j-14-plan`

## Question de recherche

Dans quelle mesure un protocole de consensus BFT garantit-il la sécurité et la
cohérence des transactions tout en maintenant des performances acceptables dans
un consortium universitaire soumis à des comportements byzantins ?

## Hypothèse

Un protocole BFT garantit la cohérence du registre malgré un nombre limité de
validateurs malveillants, mais ses performances se dégradent lorsque le nombre de
validateurs et les perturbations réseau augmentent. La dégradation attendue reste
compatible avec la vérification de diplômes, c'est-à-dire avec une finalisation
de l'ordre de quelques secondes et un débit de plusieurs transactions par seconde.

## Contexte et problème

Les universités de l'UEMOA doivent vérifier des diplômes délivrés par d'autres
établissements, parfois dans un autre pays. La vérification dépend aujourd'hui de
l'établissement émetteur, de sa disponibilité et de procédures manuelles. Une base
centrale réduirait les délais, mais créerait un point unique de défaillance et un
administrateur auquel tous devraient faire confiance. Un registre distribué entre
universités permet d'enregistrer l'empreinte d'un diplôme et de la vérifier sans
serveur central. Il reste à garantir que les universités s'accordent sur le même
registre même si l'une est compromise.

## Méthode

1. **Analyse théorique** : modèle de faute byzantine, quorums de `2f + 1` parmi
   `n = 3f + 1`, sûreté par intersection des quorums, vivacité après GST.
2. **Banc de test** : CometBFT v0.38.17 sous Docker, application `kvstore`,
   réseau de 4, 7 puis 10 validateurs représentant des universités.
3. **Réseau** : retards aller simple de 10 à 45 ms injectés avec `tc netem`
   (Dakar, Saint-Louis, Ouagadougou, Abidjan, Bamako, Niamey, Lomé, Cotonou,
   Bissau, Ziguinchor).
4. **Charge** : 20 transactions séquentielles pour la latence, 200 transactions
   avec 20 envois simultanés pour le débit, 3 essais par scénario.
5. **Scénarios** : S1 référence 4 nœuds ; S2 latence ; S3 7 et 10 nœuds ;
   S4 arrêt de `f` puis `f + 1` validateurs et reprise.
6. **Métriques** : latence moyenne, médiane, p95, débit, temps de reprise,
   nombre de messages par décision.

## Résultats attendus

- S1 : environ 1 à 1,5 s par validation, débit de l'ordre de 15 tx/s.
- S2 : quelques dizaines de millisecondes de plus seulement, car le délai entre
  blocs domine.
- S3 : augmentation modérée de la latence et légère baisse du débit ; le nombre
  de messages croît en `O(n²)` (28, 91, 190 pour 4, 7, 10).
- S4 : la chaîne continue avec `f` panne et s'arrête avec `f + 1`, sans
  bifurcation ; elle reprend après redémarrage.

## Limites annoncées

Le banc simule des pannes franches, pas un validateur qui ment activement. La
tolérance byzantine est donc démontrée théoriquement et non provoquée. Les
latences sont des ordres de grandeur, les nœuds partagent une machine et le débit
est borné par le client de mesure. Le consensus garantit l'accord, pas la véracité
du diplôme inscrit.

## Planning

| Date | Livrable |
|---|---|
| J-14 | ce plan |
| J-7 | 5 sources primaires, état de l'art |
| J-3 | diapositives, questions A14, dépôt |
| S4 (12 nov.) | exposé A9 |
| J+2 | quiz, synthèse A1, corrections |
| S5 | résultats préliminaires |
| S6 + 5 jours | article final IEEE |

## Sources de départ

Lamport, Shostak et Pease (1982) ; Castro et Liskov (1999) ; Buchman, Kwon et
Milosevic (2018) ; Yin et al. (2019) ; Androulaki et al. (2018) ; UIT-T X.1407
(2022) ; Wüst et Gervais (2018) ; documentation CometBFT.
