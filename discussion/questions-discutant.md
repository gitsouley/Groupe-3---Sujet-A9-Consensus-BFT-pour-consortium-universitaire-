# Questions de discutant — sujet A14

**Sujet discuté :** A14 — Migration post-quantique de Bitcoin et Ethereum
**Présenté par :** groupe 2 (Ndèye Gueye, Adama Sidibé, Babacar Mbaye Faye, Baye Amadou Thiam)
**Séance :** S5, vendredi 13 novembre 2026, après-midi, bloc 8 (avec A13)
**Discutants :** groupe 3 (Souleymane Kone, Mouhamadou Makhtar Gueye, Fatou Kine Thioub)

## Préparation

Les questions ci-dessous sont construites à partir du résumé d'une page du
groupe 2 (daté du 10 novembre 2026) et des tailles officielles du NIST. Elles
visent deux points où la conclusion et les chiffres se contredisent ou où la
méthode d'estimation reste implicite. Les diapositives du groupe 2 sont à lire
72 heures avant la séance ; si une réponse est déjà donnée pendant l'exposé, la
question est reformulée ou remplacée par la question de réserve.

## Question 1 — Le choix de l'algorithme est-il vraiment secondaire ?

**Question.** Votre conclusion affirme que « le vrai problème est la place dans
les blocs et le sort des fonds dormants, pas le choix de l'algorithme ». Or vos
propres chiffres donnent un débit divisé par 3,7 avec FN-DSA-512, par environ 10
avec ML-DSA-65 et par environ 15 avec SLH-DSA-128s. Comment ces deux
affirmations peuvent-elles être compatibles ? Quel algorithme recommandez-vous
pour Bitcoin, et lequel pour Ethereum, et sur quels critères ?

**Réponse attendue.**

- Une clarification de la phrase : le groupe veut probablement dire que **même
  le meilleur algorithme** laisse un surcoût structurel, donc que le choix de
  l'algorithme ne supprime pas le problème de capacité. C'est recevable, mais il
  faut alors distinguer « le choix ne supprime pas le problème » de « le choix
  n'a pas d'importance ».
- La reconnaissance que, dans leur fourchette, l'écart entre algorithmes est
  **d'un facteur 4** en débit (3,3 tx/s pour FN-DSA-512 contre 0,8 tx/s pour
  SLH-DSA-128s). Ce n'est pas neutre pour les frais, la migration et la
  pression sur les nœuds.
- Un choix argumenté : FN-DSA-512 est le moins coûteux en taille, mais sa
  normalisation (FIPS 206) et sa mise en œuvre sont plus délicates ; ML-DSA-44
  ou ML-DSA-65 offrent un compromis standardisé ; SLH-DSA-128s est réservé aux
  cas où l'on veut une hypothèse de sécurité purement fondée sur le hachage.
  Pour Ethereum, le coût en gaz et la taille de l'état comptent autant que la
  signature.

**Relance.** Si le choix de l'algorithme est secondaire, pourquoi ne pas garder
ECDSA jusqu'à l'interdiction de 2035 et migrer seulement les fonds exposés ?
Quel serait le coût de cette stratégie « minimale » ?

**Ce que nous évaluons.** La capacité à nuancer sans se contredire, la
distinction entre coût structurel et coût algorithmique, et la justification du
choix par des critères explicites (taille, standardisation, sécurité, coût de
vérification).

## Question 2 — Les 4,3 à 5,1 millions de BTC exposés sont-ils mesurés ou estimés ?

**Question.** Vous estimez entre 4,3 et 5,1 millions de BTC exposés, soit 22 à
25 % de l'offre, par type de script : 1,7 à 1,9 million en P2PK, 2,5 à 3,0
millions sur des adresses déjà dépensées, 0,1 à 0,2 million en Taproot. Or vous
indiquez ne pas mesurer adresse par adresse. D'où viennent précisément ces
fourchettes, quelle part repose sur des données de la chaîne et quelle part sur
des hypothèses ? Un fonds dormant est-il nécessairement un fonds perdu ?

**Réponse attendue.**

- L'indication de la méthode : explorateur de blocs, jeu de données public,
  étude déjà publiée, ou calcul propre à partir des sorties non dépensées.
- La séparation explicite entre **mesuré** (par exemple le nombre d'UTXO P2PK
  non dépensés) et **supposé** (par exemple la proportion de clés perdues, ou
  l'hypothèse qu'une adresse déjà dépensée reste exposée).
- La reconnaissance que « dormant » ne veut pas dire « perdu » : un fonds peut
  être détenu par un ayant droit qui ne l'a pas déplacé, et le risque quantique
  est un risque de **vol**, pas une preuve de perte. La question de gouvernance
  (geler, brûler ou laisser) doit être posée séparément.

**Relance.** Une adresse déjà utilisée est-elle exposée de la même façon qu'une
sortie P2PK ancienne ? Et si une clé est perdue, qui peut légitimement décider
de geler le fonds ?

**Ce que nous évaluons.** La traçabilité de l'estimation, la distinction
mesure/hypothèse, et la capacité à relier le chiffre à une décision de
gouvernance plutôt qu'à une simple prédiction.

## Question de réserve — La date de la menace

Votre calendrier annonce environ 2 330 qubits logiques, 2 à 4 millions de qubits
physiques et une machine entre 2032 et 2040, mais la référence correspondante
n'est pas clairement identifiée. Sur quelle source et sur quelles hypothèses
repose cette estimation ? Que devient votre conclusion si la date est repoussée
à 2050 ou avancée à 2030 ?

**Réponse attendue.** Une source primaire ou un rapport d'experts, une
distinction entre qubits logiques et physiques, et une analyse de sensibilité :
la date change l'urgence de la migration, pas la validité du risque à long
terme.

## Conduite de la discussion croisée (10 minutes)

| Temps | Action | Responsable |
|---:|---|---|
| 0–1 min | rappel du bloc A14 + A13, règle de bienveillance | Souleymane |
| 1–4 min | question 1, réponse, relance | Souleymane |
| 4–7 min | question 2, réponse, relance | Makhtar |
| 7–9 min | pont A14–A13 : preuves zk-STARK et vérification de diplômes | Fatou |
| 9–10 min | synthèse des points d'accord et de désaccord | Fatou |

**Pont avec A13.** Les preuves zk-STARK reposent sur des fonctions de hachage,
considérées comme résistantes au quantique. Peuvent-elles servir à la fois à la
vérification de diplômes (A13) et à l'agrégation de signatures post-quantiques
(A14) ? La question est à ajuster selon le contenu réel de l'exposé A13.

## Sources utilisées pour préparer les questions

- Résumé A14 du groupe 2, 10 novembre 2026.
- NIST, FIPS 204 (ML-DSA) et FIPS 205 (SLH-DSA), 2024.
- NIST, IR 8547, *Transition to Post-Quantum Cryptography Standards*.
- Aggarwal et al., « Quantum Attacks on Bitcoin, and How to Protect Against
  Them », *Ledger*, vol. 3, 2018.
- BIP-360 et discussions Ethereum sur le hard fork d'urgence.
