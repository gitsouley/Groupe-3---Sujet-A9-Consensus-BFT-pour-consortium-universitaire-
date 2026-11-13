# Démonstration A9 — scénario de 2 minutes

## Préparation (avant la séance)

```bash
docker image inspect cometbft/cometbft:v0.38.17 >/dev/null
bash code/experimenter.sh 4 --keep
```

Noter l'adresse RPC affichée, par défaut `http://localhost:36657`.

## Déroulé

1. **Montrer le consortium.** Afficher les quatre conteneurs et la hauteur
   courante :

   ```bash
   docker ps --format 'table {{.Names}}\t{{.Status}}'
   curl -s localhost:36657/status | python3 -c \
     "import json,sys; d=json.load(sys.stdin); print('hauteur', d['result']['sync_info']['latest_block_height'])"
   ```

2. **Inscrire un diplôme.** Envoyer une transaction et montrer qu'elle est
   finalisée immédiatement :

   ```bash
   curl -s 'localhost:36657/broadcast_tx_commit?tx="diplome-DEMO123=valide"'
   ```

3. **Vérifier la finalité.** Récupérer le hash renvoyé par l'étape 2 et demander
   la preuve d'inclusion du diplôme :

   ```bash
   HASH=$(curl -s 'localhost:36657/broadcast_tx_commit?tx="diplome-DEMO123=valide"' \
     | python3 -c "import json,sys; print(json.load(sys.stdin)['result']['hash'])")
   curl -s "localhost:36657/tx?hash=0x${HASH}&prove=true" | head -c 400
   ```

4. **Provoquer une panne tolérable.** Arrêter `node3`, puis envoyer une
   transaction : la chaîne continue avec trois validateurs sur quatre, soit
   exactement le quorum.

   ```bash
   docker stop node3
   curl -s 'localhost:36657/broadcast_tx_commit?tx="diplome-DEMO124=valide"'
   ```

5. **Provoquer une panne non tolérable.** Arrêter `node2` : il ne reste que deux
   validateurs, la chaîne se bloque. Montrer que la hauteur ne bouge plus.

   ```bash
   docker stop node2
   sleep 4
   curl -s localhost:36657/status | python3 -c \
     "import json,sys; d=json.load(sys.stdin); print('hauteur', d['result']['sync_info']['latest_block_height'])"
   ```

6. **Reprendre.** Redémarrer `node2` et `node3`, puis montrer que la hauteur
   repart après quelques secondes.

   ```bash
   docker start node2 node3
   sleep 10
   curl -s localhost:36657/status | python3 -c \
     "import json,sys; d=json.load(sys.stdin); print('hauteur', d['result']['sync_info']['latest_block_height'])"
   ```

## Plan de secours

Si Docker ou le réseau ne fonctionne pas en séance :

- montrer `resultats/figures/fig5_pannes.pdf` et commenter la chronologie réelle ;
- montrer `resultats/mesures_agregees.csv` et le tableau de l'article ;
- expliquer que les mesures ont été faites sur le même banc, avec les scripts du
  dépôt, et que les figures sont régénérées par `bash code/reproduire.sh`.

Ne jamais lancer d'attaque contre un système réel. La démonstration reste sur le
réseau de test local, avec des identifiants de diplômes synthétiques.
