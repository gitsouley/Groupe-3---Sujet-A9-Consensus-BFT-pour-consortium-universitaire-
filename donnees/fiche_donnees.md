# Fiche des données

## Origine

Les données de `resultats/mesures_brutes.csv` et
`resultats/timeline_pannes.csv` ont été produites par le groupe 3 sur un banc
CometBFT v0.38.17 local, les 11 et 13 novembre 2026. Aucune donnée n'est
simulée dans ces deux fichiers.

Les données de `donnees/latences_villes.csv` sont des **paramètres injectés**
avec `tc netem`. Ce sont des ordres de grandeur inspirés des distances
régionales, pas des mesures de terrain. Elles sont utilisées pour tester la
sensibilité du consensus, pas pour affirmer une latence réelle entre universités.

## Fichiers

| Fichier | Contenu | Nature |
|---|---|---|
| `latences_villes.csv` | 10 nœuds, ville, retard aller simple, gigue | paramètres |
| `scenarios.csv` | scénarios S1 à S4, charge, nombre d'essais | protocole |
| `resultats/mesures_brutes.csv` | 17 lignes d'essais, latence, p95, débit, tx | mesuré |
| `resultats/timeline_pannes.csv` | 78 points, hauteur de bloc toutes les 0,5 s | mesuré |
| `resultats/mesures_agregees.csv` | moyenne, écart-type, IC95, p95, débit | calculé |
| `resultats/analyse_theorique.csv` | n, f, quorum, messages, marge | calculé |

## Variables

- `scenario` : S1 référence, S2 latence, S3 nombre de validateurs, S4 pannes.
- `n` : nombre de validateurs.
- `panne` : nombre de validateurs arrêtés.
- `latence_moy_ms` : moyenne des temps de `broadcast_tx_commit`.
- `p95_ms` : 95ᵉ centile des latences de l'essai.
- `debit_tx_s` : transactions validées par seconde.
- `tx_ok`, `tx_total` : transactions acceptées sur transactions envoyées.
- `hauteur_avant`, `hauteur_apres` : hauteur de bloc avant et après l'essai.
- `reprise_s` : délai entre le redémarrage et le premier nouveau bloc.
- `phase` : phase de la chronologie (`nominal`, `f-1 panne`, `f+1 pannes`,
  `reprise`).

## Traitements

1. Les latences sont mesurées par `time.perf_counter()` autour de la requête
   HTTP `broadcast_tx_commit`.
2. Le p95 est calculé sur les latences triées, indice
   `max(0, int(0.95 * N) - 1)`.
3. Les agrégats utilisent la moyenne des 3 essais, l'écart-type d'échantillon et
   un intervalle de confiance à 95 % avec `t = 4,303` pour `dl = 2`.
4. Les figures sont produites par `code/analyser.py` et
   `code/tracer_resultats.py`.

## Limites

- Les validateurs partagent une seule machine (8 cœurs, 10 Go de RAM).
- Le client de mesure est en Python et utilise 20 envois simultanés ; le débit
  mesuré est donc borné par le client, pas par CometBFT.
- Les pannes sont des arrêts de conteneur, pas des fautes byzantines actives.
- Le `timeout_commit` de CometBFT est de 1 s : la latence observée inclut ce
  délai incompressible.
- La gigue de 5 ms est ajoutée uniformément ; elle ne modélise pas les rafales
  de perte de paquets.
