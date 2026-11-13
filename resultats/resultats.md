# Résultats — synthèse pour l'article et les diapositives

Tous les chiffres ci-dessous proviennent de `mesures_agregees.csv` et
`timeline_pannes.csv`, régénérés par `bash code/reproduire.sh`.

## 1. Latence et débit

| Scénario | n | Pannes | Latence moyenne | p95 | Débit | Essais |
|---|---:|---:|---:|---:|---:|---:|
| S1 — référence, sans retard | 4 | 0 | 1 303 ms ± 9 ms | 1 317 ms | 15,3 tx/s | 3 × 200 tx |
| S2 — latence UEMOA | 4 | 0 | 1 365 ms ± 27 ms | 1 417 ms | 14,6 tx/s | 3 × 200 tx |
| S3 — sept validateurs | 7 | 0 | 1 403 ms ± 29 ms | 1 503 ms | 14,1 tx/s | 3 × 200 tx |
| S3 — dix validateurs | 10 | 0 | 1 401 ms ± 16 ms | 1 526 ms | 14,1 tx/s | 3 × 200 tx |
| S4 — un validateur arrêté | 4 | 1 | 2 258 ms ± 227 ms | 5 698 ms | 5,9 tx/s | 3 × 50 tx |
| S4 — deux validateurs arrêtés | 4 | 2 | chaîne bloquée | — | 0 tx/s | 2 essais |

Lecture : le passage de 4 à 10 validateurs coûte environ **7,5 %** de latence
moyenne et **7,8 %** de débit par rapport à S1. Le retard réseau ajoute environ
**4,8 %** de latence moyenne entre S1 et S2. En revanche, l'arrêt de `f = 1`
validateur multiplie la moyenne par **1,73** et divise le débit par **2,6**, avec
une queue p95 à **5,7 s**. L'arrêt de `f + 1 = 2` validateurs bloque la chaîne.

## 2. Pannes et reprise

- Avec `f = 1` panne : la hauteur continue d'avancer ; aucune bifurcation n'est
  observée ; les 50 transactions de l'essai sont validées.
- Avec `f + 1 = 2` pannes : la hauteur reste constante, les transactions
  échouent, aucun bloc n'est produit.
- Après redémarrage : le premier nouveau bloc apparaît après **8,6 s** dans
  l'essai chronométré. La chaîne reprend à la hauteur suivante, sans rollback
  visible.
- Journal détaillé : `timeline_pannes.csv` (78 points, 0,5 s d'intervalle).

## 3. Coût en messages

Le calcul PBFT `2n² − n` donne :

| n | f | Quorum | Messages par décision |
|---:|---:|---:|---:|
| 4 | 1 | 3 | 28 |
| 7 | 2 | 5 | 91 |
| 10 | 3 | 7 | 190 |

Le passage de 4 à 10 validateurs multiplie le nombre de messages par **6,8**
alors que le débit ne baisse que de **7,8 %** dans notre banc. Cela suggère que
le coût `O(n²)` n'est pas encore le facteur limitant à cette échelle, et que le
`timeout_commit` et le client de mesure dominent.

## 4. Interprétation

1. **Sûreté :** aucune divergence observée, y compris pendant les pannes. C'est
   cohérent avec l'intersection des quorums (`f + 1` nœuds communs).
2. **Vivacité :** elle tient tant que `n − pannes ≥ 2f + 1` ; elle casse dès que
   `pannes = f + 1` dans notre configuration à 4 nœuds.
3. **Performance :** la latence reste de l'ordre de 1,3 à 1,5 s pour 4 à 10
   validateurs, ce qui est compatible avec une vérification de diplôme. La
   dégradation en panne reste sous 2,3 s en moyenne, mais la queue p95 dépasse
   5 s.
4. **Limite :** le banc ne teste pas un validateur qui ment. La tolérance
   byzantine est argumentée, pas provoquée.

## 5. Figures

- `fig1_quorums.pdf` : intersection de quorums et tailles pour n = 4, 7, 10.
- `fig2_phases_pbft.pdf` : séquence simplifiée de PBFT.
- `fig3_latence.pdf` : latence moyenne et p95 par scénario.
- `fig4_debit.pdf` : débit par scénario, y compris le cas bloqué.
- `fig5_pannes.pdf` : hauteur de bloc pendant les arrêts et la reprise.
- `fig6_messages.pdf` : croissance `O(n²)` du nombre de messages.
