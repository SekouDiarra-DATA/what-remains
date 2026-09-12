# Architecture de l'agent

> À compléter le jour du hackathon, une fois l'idée et la stack finalisées.

## Schéma global
_(à insérer : diagramme du flux — canal d'entrée → agent → outils/API → sortie)_

## Composants

| Composant | Rôle | Technologie |
|---|---|---|
| Canal d'intégration | Où vit l'agent (Slack, email, navigateur, etc.) | |
| Orchestrateur / logique agent | Décision, appels d'outils | |
| Modèle LLM | Raisonnement | |
| Outils / connecteurs | Accès aux données ou actions externes | |
| Mémoire / contexte | Ce qui rend l'agent utile dans son environnement | |

## Flux de données
1. Déclencheur (événement, message, action utilisateur)
2. Traitement par l'agent
3. Appel(s) d'outils / API externes
4. Réponse ou action dans le canal d'origine

## Décisions techniques et justifications
_(pourquoi ce canal, pourquoi cette stack, contraintes du hackathon — 4h de build)_
