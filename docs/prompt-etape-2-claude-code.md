# Instructions pour Claude Code

## Étape 1 — Lecture, analyse et compréhension (obligatoire avant toute autre action)

Le fichier `brief-produit-digital-closure-v2-exhaustif.md`, situé dans ce dossier de projet, est le document produit complet de mon projet de hackathon. Avant de produire quoi que ce soit d'autre, tu dois :

1. Lire l'intégralité du document, du préambule jusqu'au glossaire final — ne saute aucune section, y compris les parties qui semblent secondaires (scénarios d'usage, cas limites, considérations éthiques, glossaire)
2. Prendre le temps de vraiment comprendre : le problème que le produit résout, pourquoi il est important (les chiffres cités doivent être intégrés à ta compréhension, pas seulement lus), qui sont les utilisateurs et dans quel état émotionnel ils se trouvent, ce que le produit s'interdit explicitement de faire (section 4.3 et section 9), et les contraintes strictes du hackathon (section 1.4 et 1.5)
3. Une fois ta lecture terminée, restitue-moi un résumé de ta compréhension en 10 à 15 lignes maximum, dans tes propres mots, qui couvre : le problème, la cible principale, l'angle différenciant par rapport à l'existant, et les trois contraintes non négociables que tu as identifiées (technique, éthique, et de format hackathon). Ce résumé me permet de vérifier que tu as bien saisi l'esprit du projet avant que tu ne passes à l'étape suivante.

**Ne passe pas à l'étape 2 tant que je n'ai pas validé ce résumé.**

## Étape 2 — Une fois ma validation reçue : cahier des charges technique et plan de construction

Après ma validation, produis un cahier des charges technique complet et un plan de construction, structurés selon ta propre expertise d'ingénieur, mais qui doivent impérativement :

- Rester fidèles à chaque contrainte, limite et principe éthique énoncés dans le document produit (notamment : aucune action irréversible automatisée, MVP volontairement circonscrit, ton sobre)
- Être réalisables dans la fenêtre de temps réelle du hackathon (environ 4h15 de développement effectif)
- Proposer une architecture technique concrète (choix de stack, découpage en modules ou en étapes, ce qui est fait avec des données simulées vs réelles, ce qui est démontrable vs ce qui reste conceptuel pour la démo)
- Inclure un plan de construction séquencé dans le temps (par exemple : quoi construire dans la première heure, la deuxième, etc., avec des jalons de vérification)
- Identifier clairement les risques techniques qui pourraient faire échouer la démo dans le temps imparti, et proposer un plan de repli (fallback) pour chacun
- Se terminer par une liste des décisions techniques qui restent ouvertes et nécessitent mon arbitrage avant que tu commences à coder

Pose-moi toutes les questions nécessaires à ce stade si un point du brief te semble ambigu pour la conception technique, plutôt que de deviner.
