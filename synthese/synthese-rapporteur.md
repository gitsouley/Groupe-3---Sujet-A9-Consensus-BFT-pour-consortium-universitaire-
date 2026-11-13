# Synthèse du rapporteur — A1 : modes AES dans les applications de paiement mobile

**Séance :** S3, mercredi 11 novembre 2026, bloc 1
**Présentateurs (groupe 7) :** Mouhamadou Rassoul Name, Ousmane Diallo, Ndèye Penda Niang
**Discutants :** groupe 4 — **Rapporteurs :** groupe 3 (Souleymane Kone, Mouhamadou Makhtar Gueye, Fatou Kine Thioub)

## Sujet et question

Le paiement mobile est central dans l'UEMOA : la BCEAO recense 60,6 millions de
comptes de monnaie électronique actifs fin 2025 et 160 415 milliards de FCFA
échangés en 2024. Les échanges entre l'application et le serveur reposent sur du
chiffrement. Le groupe 7 demande **quelle part des applications Android de
paiement utilisées en Afrique de l'Ouest commet des erreurs de chiffrement**. Son
hypothèse, appuyée sur Egele et al. (CCS 2013), est qu'une part importante en
commet au moins une — 88 % des applications Android utilisant des API
cryptographiques dans cette étude. L'étude de référence ne portait toutefois ni
sur le paiement ni sur l'Afrique de l'Ouest, ce qui justifie le projet.

## Message central

**AES n'est pas cassé : ce sont les usages qui cassent la sécurité.** AES ne
chiffre qu'un bloc de 16 octets ; c'est le mode opératoire, avec un IV ou un
nonce, qui protège un message entier. ECB ne protège pas les motifs. CBC et CTR
assurent la confidentialité si l'IV ou le nonce est correct, mais pas
l'intégrité. GCM assure les deux, sauf si le nonce est réutilisé. Le groupe
étudie cinq erreurs et, pour chacune, le modèle d'attaque le plus faible qui
suffit : ECB par défaut en Java (COA), IV constant ou prévisible en CBC (CPA),
nonce réutilisé en CTR ou GCM (KPA), clé écrite dans l'APK (la décompilation
suffit) et chiffrement sans intégrité (CCA, oracle de remplissage).

Les démonstrations, sur données synthétiques et avec un script Python
reproductible, sont convaincantes : le logo de l'ESP reste lisible en ECB ; le
jeu IND-CPA donne un avantage de 1 dès que l'IV ou le nonce est fixe, et proche
de 0 s'il est aléatoire ; un nonce réutilisé permet de lire un message sans la
clé ; en CTR, un bit modifié change « 5000 » en « 9000 » sans être détecté,
alors que GCM rejette le message ; un message CBC est déchiffré par oracle de
remplissage en environ 6 000 requêtes.

## Méthode et état d'avancement

Le protocole est fixé à l'avance : corpus d'APK publiques (paiement, diffusion
publique, usage dans l'UEMOA, version figée et empreinte SHA-256), analyse
statique uniquement, taxonomie de 11 erreurs en 5 familles, et métriques
chiffrées (prévalence avec intervalle de confiance à 95 %, fréquence par erreur,
origine application ou bibliothèque, précision et rappel de l'outil). Le pilote
porte sur 12 applications financières open source tirées au hasard sur F-Droid :
10 analysables, 5 utilisant le chiffrement, **0 erreur trouvée, IC 95 %
[0 ; 43 %]**. Le groupe conclut honnêtement que c'est trop peu pour répondre à la
question ; le pilote valide surtout la chaîne d'analyse, dont le détecteur a été
corrigé (un faux positif, puis des faux négatifs) avant toute mesure. La
prochaine étape est l'analyse d'applications de paiement ouest-africaines. Le
cadre éthique est explicite : Wave et Orange Money servent de contexte et n'ont
pas été testées ; aucune application vulnérable ne sera nommée sans signalement
privé préalable.

## Discussion

Les discutants du groupe 4 et la salle ont interrogé la représentativité du
pilote et la détection statique de la réutilisation de nonce, qui dépend de
l'exécution. L'enseignant a rappelé qu'une alerte statique est un indice, pas
une preuve, et que la sécurité peut être déléguée à TLS. La discussion croisée
avec A2 a relié les modes opératoires au stockage des clés.

## Bilan critique

**Points forts.** Le sujet est ancré dans le contexte ouest-africain. La
démonstration est complète, chiffrée et reproductible ; elle prouve clairement
le message central. La méthode est rigoureuse : critères fixés à l'avance, outil
validé avant mesure, limites reconnues et démarche éthique.

**Points à renforcer.** La question de recherche reste sans réponse, car le
pilote ne contient aucune application de mobile money. L'accès aux APK de Google
Play, l'obfuscation et le code natif (Flutter, React Native) pourraient réduire
fortement la part analysable. La méthode de l'intervalle de confiance n'est pas
précisée. La source BCEAO est incomplète. Enfin, une application qui confie
toute la sécurité à TLS doit être explicitement classée « sans erreur d'usage
AES » ou exclue du corpus, sinon la prévalence est ambiguë.

**À retenir.** AES-GCM (ou ChaCha20-Poly1305), un nonce jamais réutilisé et une
clé hors du code. Une alerte d'analyse statique est un indice à vérifier, pas la
preuve d'une faille.
