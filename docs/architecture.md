# Cahier des charges technique — What Remains

> Rédigé à partir du brief produit v2 exhaustif, validé le 12/09/2026. Mis à jour après le pivot "agent enquêteur" (voir section 0bis).

---

## 0. Rappel des contraintes non négociables (ce document s'y conforme strictement)

1. **Aucune action irréversible automatisée.** L'agent ne fait jamais qu'analyser, classer, proposer. Aucun bouton de l'interface n'envoie, ne résilie, ni ne modifie quoi que ce soit à distance.
2. **MVP volontairement circonscrit.** Un seul scénario (Scénario A — décès soudain), un seul canal (email), un jeu de données simulé, une seule langue de démo (anglais).
3. **Ton sobre en toute circonstance.**
4. **Fenêtre de temps réelle limitée** — chaque choix technique est fait pour minimiser le risque et maximiser ce qui est démontrable.

---

## 0bis. Pivot : d'un agent "trieur" à un agent "enquêteur"

**Constat qui a motivé le changement** : classifier chaque email indépendamment (email → catégorie) ne se distingue pas des dizaines d'assistants de tri de boîte mail déjà existants. Le barème du hackathon récompense une **nouvelle interaction**, pas seulement un nouvel environnement — et le tri email par email n'en est pas une.

**Ce qui change concrètement :**

1. **Synthèse multi-emails au lieu de classification email par email.** L'agent regroupe d'abord les emails par service, puis reconstruit un seul profil de compte à partir de *toutes* les preuves disponibles pour ce service (inscription, hausse de prix, dernière facture → un historique cohérent). C'est un travail d'agrégation et de synthèse, pas de tri local.
2. **Guide de résiliation curaté pour les marques réelles du jeu de données.** Plutôt qu'un brouillon générique, l'agent restitue les vraies étapes de résiliation pour les services reconnaissables (Netflix, Google One, Adobe), et répond honnêtement "procédure non trouvée, contactez le fournisseur" pour les autres. Choix assumé : **pas de recherche web live (Exa)** pendant le hackathon — trop de risque technique pour le temps restant ; le guide est une base de connaissances statique que nous avons rédigée nous-mêmes. C'est aussi plus honnête que du scraping live non vérifié, ce qui reste cohérent avec le principe éthique du brief (9.4 — jamais affirmer une information précise qu'on ne peut garantir).

Cette évolution reste conforme à toutes les contraintes de la section 0 : toujours aucune action automatisée, toujours un MVP circonscrit (2 à 4 marques dans le guide, pas une couverture exhaustive), toujours un ton sobre.

---

## 1. Architecture technique

### 1.1 Stack retenue

| Couche | Choix |
|---|---|
| Langage | Python 3.10+ (utilise `list[dict]`, `X \| None`) |
| Interface | Streamlit, CSS injecté + `.streamlit/config.toml` |
| Intelligence (synthèse, brouillon, guide) | API compatible OpenAI — OpenRouter en production (`openai/gpt-4o-mini`) |
| Ingestion | Import JSON simulé (chemin principal de démo) **ou** connexion Gmail OAuth réelle en lecture seule (chemin bonus, robustesse) |
| Données | `data/demo_emails.json` (12 emails) + `data/cancellation_guides.json` (4 marques, enrichi via Exa) |
| Persistance | `st.session_state` uniquement |
| Export | CSV **et** PDF complet (`fpdf2`) via `st.download_button` |

### 1.2 Découpage en modules (état réel du code)

```
data/
├── demo_emails.json          # 12 emails simulés — 3 services avec historique multi-emails
├── cancellation_guides.json  # guide curaté (Netflix, Google One, Adobe, Spotify)
├── analysis_cache.json       # résultat pré-calculé du jeu de démo (fiabilité de la démo)
├── gmail_oauth_credentials.json / gmail_token.pickle  # non commités, voir .gitignore

src/
├── app.py                    # Interface Streamlit — orchestre tout le parcours
├── engine/
│   ├── classifier.py         # Regroupe par (domaine + nom normalisé) + synthétise un profil par LLM
│   ├── resolver.py           # Lookup (exact puis partiel) du guide de résiliation curaté
│   ├── prioritizer.py        # Tri des comptes par urgence décroissante
│   ├── drafter.py            # Génère un message de contact quand aucun guide n'existe
│   ├── gmail_client.py       # Connexion Gmail OAuth lecture seule (chemin bonus)
│   └── report.py             # Génère le rapport PDF complet (fpdf2)
├── prompts/
│   ├── synthesize.txt        # Prompt système de synthèse multi-emails
│   ├── draft.txt             # Prompt système de génération de brouillon
│   └── guide_from_research.txt  # Prompt de distillation des résultats Exa en guide
└── scripts/
    └── research_cancellation_guide.py  # Recherche Exa + synthèse LLM → cancellation_guides.json
```

### 1.3 Flux de données

```
demo_emails.json  (ou emails Gmail réels via gmail_client.fetch_recent_emails())
      │
      ▼
group_by_service()  →  regroupe par (DOMAINE d'expéditeur + nom affiché normalisé —
      │                  voir section 2 : upgrade en deux temps après les tests sur
      │                  une vraie boîte), trie chaque groupe par date
      ▼
synthesize_account() →  1 appel LLM par service, sur TOUTES ses emails :
      │                  {service_name, category, status, urgency, evidence,
      │                   reasoning, history_summary, source_email_ids}
      ▼
sort_by_urgency()   →  tri décroissant
      │
      ▼
   app.py (checklist priorisée, un compte = une ligne, pas un email = une ligne)
      │
      ▼ (sur clic utilisateur, par compte)
resolver.get_cancellation_guide(service_name)
      │
      ├── trouvé  → affiche les étapes réelles + lien officiel + note de prudence
      └── absent  → drafter.generate_draft() propose un message honnête, éditable, non envoyé
      │
      ▼
   app.py → export CSV (checklist) ou PDF complet (report.build_pdf_report,
             inclut preuves, historique, guides et brouillons générés)
```

### 1.4 Schéma de données (contrat `classifier.py` → reste de l'app)

```json
{
  "service_name": "Netflix",
  "category": "subscription",
  "status": "certain",
  "urgency": "high",
  "evidence": "Recurring monthly payments confirmed, most recently on 2026-08-28.",
  "reasoning": "Automatic recurring payment with no evidence of cancellation.",
  "history_summary": "Active since November 2025; price increased in July 2026.",
  "source_email_ids": ["e1", "e2", "e3"],
  "last_email_date": "2026-08-28"
}
```

---

## 2. Répartition simulé vs réel, démontrable vs conceptuel

| Élément | Statut |
|---|---|
| Boîte email source (chemin principal, démo) | Simulée (`data/demo_emails.json`) — action mise en avant dans l'UI : "Try a sample inbox" |
| Boîte email source (chemin bonus) | **Réelle**, via OAuth Gmail lecture seule — validée sur une vraie boîte (20 comptes détectés), non utilisée dans la vidéo publique |
| Regroupement par service | **Réel**, par (domaine d'expéditeur + nom affiché normalisé) — upgrade en deux temps depuis `from_name` exact, décidé après le test Gmail réel |
| Synthèse multi-emails | **Réelle**, cœur démontrable du pivot |
| Guide de résiliation | **Réel mais curaté** (Netflix, Google One, Adobe, Spotify), enrichi hors-ligne via Exa — pas de recherche live, fallback honnête pour le reste |
| Génération de brouillon (`drafter.py`) | **Réelle**, construite et testée |
| Export PDF complet (`report.py`) | **Réel**, construit et testé |
| Reprise de session, multi-famille, export notaire séparé | Conceptuel uniquement, non implémenté |

---

## 3. Plan de construction révisé (post-pivot, ~2h30 restantes au moment du pivot)

| Bloc | Durée indicative | Objectif | Jalon |
|---|---|---|---|
| **1** ✅ | 30 min | Dataset enrichi, `classifier.py` restructuré, `resolver.py`, `prioritizer.py` — testé via `python src/engine/classifier.py` | Netflix et Google One ressortent avec un `history_summary` cohérent citant plusieurs emails ; StyleHub/YogaFlow restent "uncertain" |
| **2** ✅ | 40 min | `app.py` : écran de consentement → import → progression → checklist priorisée par compte, badges certain/incertain, drill-down montrant les emails sources | Parcours cliquable de bout en bout, testé dans le navigateur |
| **3** ✅ | 30 min | `drafter.py` + guide de résiliation intégré à l'UI + export CSV + **cache d'analyse** (`data/analysis_cache.json`, voir risque n°2) | Netflix/Google One/Adobe affichent les vraies étapes ; FitZone/Northgate/StyleHub/YogaFlow affichent le fallback honnête + bouton de brouillon fonctionnel ; CSV exportable |
| **4** — en cours | 30-40 min | Relecture de ton (grille section 10.2 du brief), répétition chronométrée, enregistrement vidéo 2 min, rédaction de la description de soumission + post réseaux sociaux | Vidéo prête, texte de soumission prêt |

**Ajout non prévu au plan initial mais nécessaire** : gestion des quotas/coûts API (OpenAI → Gemini free tier → OpenRouter avec crédits sponsors) a pris plus de temps que budgété. Le cache d'analyse (`get_accounts()` dans `classifier.py`) élimine ce risque pour la suite : l'app ne rappelle plus l'API à chaque clic.

**Design final (post-Bloc 3)** : identité visuelle produite par YouWare AI à partir du prompt de [`docs/design_prompt.md`](design_prompt.md) — palette "document sobre" (papier chaud, encre ardoise, accents minéraux), zéro emoji, priorité/statut communiqués par bordure + libellé texte plutôt que rouge/vert. CSS injecté dans `app.py`, `.streamlit/config.toml` ajouté. Testé et validé visuellement dans le navigateur (bandeau de réassurance, cartes à bordure colorée, tags, brouillon éditable).

**Bonus post-Bloc 3 (validation de robustesse)** : ajout d'une seconde voie d'ingestion — connexion OAuth Gmail réelle, lecture seule (`engine/gmail_client.py`), en complément du JSON simulé (pas en remplacement). Testée avec succès sur une vraie boîte mail : 20 services détectés, dont 2 correctement "certain" (Google Play, KoboToolbox) et 18 honnêtement "uncertain". Corrige au passage un bug réel découvert par ce test (deux comptes avec le même `service_name` généré par le LLM cassaient les clés de widgets Streamlit — corrigé par un index unique par ligne). **Ce chemin Gmail ne doit pas être montré dans la vidéo de démo publique** (données personnelles réelles) — il reste un argument oral de robustesse, pas un élément de la démo filmée.

**Restructuration "produit fini" (post-design)** : la connexion Gmail est devenue l'action principale de l'écran d'accueil (bouton primaire "Connect a Gmail account"), le jeu de données simulé est relégué dans un tiroir secondaire replié ("No account to connect right now? Try a sample inbox"). Ajout d'une gestion d'erreur honnête sur tout le chemin Gmail (échec de connexion, fichier de credentials manquant, boîte vide — cas limite 8.2 du brief) au lieu de laisser remonter une trace Python brute. **Pour l'enregistrement de la vidéo, c'est bien le tiroir "Try a sample inbox" qu'il faut utiliser**, pas le bouton Gmail principal.

**Export PDF complet (`engine/report.py`)** : en plus du CSV, un bouton "Download full report as PDF" génère un document complet (résumé, un bloc par compte avec preuves/historique/guide ou brouillon inclus, avertissement légal final) dans la même palette que l'app. Choix technique : `fpdf2` (polices core PDF uniquement, zéro dépendance système) plutôt qu'un moteur HTML→PDF type WeasyPrint, pour éviter tout risque d'installation sous Windows à ce stade critique du projet.

**Audit de fin de session** : vérification approfondie de tous les fichiers (documentation, code, configuration). Correctifs appliqués : regroupement par domaine au lieu du nom d'affichage (voir section 2), modèle Gemini déprécié corrigé dans `.env.example`, fichiers de référence déplacés dans `docs/` pour la propreté du dépôt, `.gitignore` complété (`.streamlit/secrets.toml` en prévision d'un déploiement cloud), vérification qu'aucun secret ou donnée personnelle n'a jamais été commité (voir section 6). Ajout d'un bouton "← Back" visible en haut de l'écran de résultats (le seul retour existant, "Start over", était enterré en bas de page).

**Audit indépendant par Codex** (voir [`docs/codex_audit_prompt.md`](codex_audit_prompt.md)) — a trouvé plusieurs vrais bugs que notre propre audit avait manqués. Corrections appliquées :
- **Regroupement par domaine seul fusionnait des services distincts** (ex. Google One + Google Play sous `google.com`). Corrigé : clé de regroupement = (domaine, nom d'affichage) — ni l'un ni l'autre seul ne suffit, voir `classifier.py`.
- **Sortie LLM jamais validée** avant d'être consommée par l'UI (risque de crash sur JSON malformé). Corrigé : valeurs par défaut sûres pour chaque champ dans `synthesize_account`.
- **Correspondance floue du guide de résiliation trop permissive** (une chaîne vide matchait Netflix ; "ad" matchait Adobe). Corrigé : correspondance par mots entiers (`resolver.py`), contradiction directe avec le principe "pas de fausse certitude" du brief.
- **Brouillon disponible même pour un compte "Unconfirmed"**, affirmant un décès pour clôturer un compte non confirmé — contraire au brief. Corrigé : le bouton de brouillon n'apparaît que pour les comptes "certain".
- **Injection CSV possible** (valeurs LLM commençant par `=`, `+`, `-`, `@` interprétables comme formule dans Excel). Corrigé : préfixe d'échappement dans `build_csv`.
- **Consentement incomplet** : ne mentionnait pas qu'un fournisseur IA externe traite le contenu des emails. Ajouté à l'écran de consentement.
- **Brouillon édité à l'écran non synchronisé avec l'export PDF** (le PDF gardait la version générée, pas la version éditée par l'utilisateur). Corrigé.
- **Chemin Gmail limité aux 60 emails les plus récents**, sans recherche ciblée — une preuve ancienne pouvait être invisible. Corrigé : recherche par mots-clés de facturation (`BILLING_QUERY`) + pagination jusqu'à 150 résultats dans `gmail_client.py`.
- **Écart doc/code** : l'architecture revendiquait un "drill-down montrant les emails sources" qui n'existait pas dans l'UI (seul un compte s'affichait). Corrigé : chaque compte affiche maintenant la date et le sujet de chaque email source (`classifier.py` stocke `source_emails`, `app.py` les affiche).

Non corrigé, assumé : `_clean()` dans `report.py` remplace les caractères hors Latin-1 par `?` dans le PDF (limite pour des noms non latins, hors scope MVP anglophone) ; le cache de démo ne vérifie pas qu'il correspond aux emails reçus (acceptable car le jeu de données de démo est fixe et documenté comme tel).

**Second tour d'audit Codex** — a vérifié les correctifs ci-dessus et en a trouvé trois de plus :
- **La clé (domaine, nom exact) réintroduisait une fragmentation** : "Netflix" et "The Netflix Team" depuis le même domaine devenaient deux comptes distincts. Corrigé : le nom est normalisé (mots génériques comme "the", "team", "support" retirés) avant comparaison — "Netflix" et "The Netflix Team" convergent, mais "Google One" et "Google Play" restent distincts.
- **`json.loads()` sans `try/except`** pouvait faire échouer toute l'analyse sur une réponse non-JSON. Corrigé : repli sur un enregistrement "uncertain/low" sûr plutôt qu'un crash.
- **Formulations "every trace" / "whole inbox" trop fortes** dans le README vu que le chemin Gmail ne couvre que les emails correspondant à des mots-clés de facturation, pas un scan exhaustif. Corrigé : reformulé en "relevant billing-related traces found in the analyzed inbox".

Confirmé comme risque accepté (pas de correctif) : l'injection de prompt via le contenu d'un email reste possible en théorie, mais l'absence totale d'action autonome et la distinction explicite certain/incertain limitent l'impact réel — cohérent avec le principe du brief de ne jamais agir sans validation humaine.

**Limite non résolue à garder à l'esprit hors hackathon** : `BILLING_QUERY` dans `gmail_client.py` est en anglais uniquement — une boîte mail dans une autre langue ne matchera pas ces mots-clés. Pertinent si le projet est repris au-delà du MVP (voir aussi section 7 sur le déploiement public).

---

## 4. Risques techniques et plans de repli

| # | Risque | Plan de repli |
|---|---|---|
| 1 | Synthèse LLM incohérente sur les groupes multi-emails | Prompt déjà conservateur (`status: uncertain` par défaut sauf preuve claire) ; tester sur le jeu de données avant de construire l'UI dessus |
| 2 | Latence/échec API pendant l'enregistrement de la vidéo | **Résolu** : `data/analysis_cache.json` généré à l'avance, l'app le charge instantanément — plus aucun appel API live lors des clics de démo |
| 3 | Le guide curaté (4 marques) peut sembler "codé en dur" si un juge technique regarde le code de près | Assumer et retourner l'argument dans le pitch : plus honnête et plus sûr qu'un scraping live non vérifié pour une v1 ; mentionner Exa comme évolution naturelle |
| 4 | ~~Le regroupement par `from_name` est une simplification~~ | **Résolu** : regroupement par (domaine + nom affiché normalisé), affiné en deux passes après le test sur une vraie boîte Gmail (voir historique d'audit ci-dessus pour le détail des deux itérations) |
| 7 | Le flux OAuth Gmail actuel (`run_local_server`, jeton unique sur disque) n'est pas sûr pour un déploiement web multi-utilisateurs | Assumé : ce chemin reste un usage local/développeur uniquement. Ne jamais déployer ce code tel quel sur un serveur public partagé — voir section 7 |
| 5 | Dérive de ton sous pression de temps | Passe de relecture non-négociable en Bloc 4 |
| 6 | Bloc 4 (polish + tournage + rédaction) déborde | Script de pitch rédigé et chronométré dès que possible pendant les temps morts des Blocs 2-3 |

---

## 5. Décisions techniques (toutes résolues)

| Décision | Choix retenu |
|---|---|
| Fournisseur LLM | OpenRouter (crédits sponsors hackathon) |
| Langue interface/démo | Anglais |
| Ingestion email | Import JSON simulé |
| Export | CSV |
| Contenu du jeu de données | 12 emails, 3 comptes avec historique multi-emails (Netflix, Google One, Spotify) |
| Nom du projet | **What Remains** |
| Architecture de classification | Synthèse multi-emails par service (pivot du 12/09) |
| Recherche de procédure de résiliation | Guide curaté (Netflix, Google One, Adobe, Spotify), enrichi hors-ligne via Exa + synthèse LLM — pas de recherche live dans l'app |
| Fiabilité démo | Cache d'analyse pré-calculé (`data/analysis_cache.json`), zéro appel API live pendant le tournage |
| Regroupement des emails | Par (domaine d'expéditeur + nom affiché normalisé) — upgrade en deux temps post-tests Gmail réel |
| Hiérarchie de l'écran de connexion | Gmail réel en action principale, jeu de démo en option secondaire repliée |
| Export du livrable final | CSV **et** PDF complet (`fpdf2`) |

Plus aucune décision bloquante.

---

## 6. Audit de sécurité — données personnelles et secrets

Vérification effectuée avant tout push public sur GitHub :

- `data/gmail_token.pickle` (jeton d'accès réel) et `data/gmail_oauth_credentials.json` : **jamais trackés, jamais committés**, y compris dans l'historique complet (`git log --all --full-history`) — correctement listés dans `.gitignore`.
- `data/analysis_cache.json` : contient uniquement les 8 comptes du jeu de données **simulé** — aucune trace des résultats du test sur la vraie boîte Gmail (ce test n'a jamais existé que dans la mémoire de la session Streamlit, jamais écrit sur disque).
- Recherche par mot-clé dans tout le dépôt (noms d'organisations vus lors du test Gmail réel) : aucun résultat.
- `.gitignore` couvre également `.streamlit/secrets.toml`, en prévision d'un futur déploiement sur Streamlit Community Cloud (c'est l'emplacement standard où Streamlit Cloud attend les secrets — il ne doit jamais être commité).

**Conclusion** : le dépôt peut être poussé en public sans risque pour les comptes personnels utilisés pendant le développement.

---

## 7. Limites connues pour un déploiement public (au-delà du hackathon)

Deux contraintes réelles, non résolues par du code, à garder en tête si le projet est repris après le hackathon :

1. **Vérification Google OAuth.** L'app Google Cloud est en mode "Test" (max 100 utilisateurs ajoutés manuellement). Autoriser n'importe quel utilisateur Gmail au monde nécessite une vérification Google (politique de confidentialité, domaine vérifié, revue de sécurité) — un processus de plusieurs jours à plusieurs semaines, indépendant de la qualité du code.
2. **Le flux OAuth actuel n'est pas multi-utilisateurs.** `gmail_client.py` utilise `InstalledAppFlow.run_local_server()` (flux "desktop", ouvre un navigateur sur la machine qui exécute le serveur) et stocke un seul jeton partagé dans `data/gmail_token.pickle`. Déployé tel quel sur un serveur public, tous les visiteurs partageraient le même compte connecté. Pour un vrai déploiement multi-utilisateurs, il faudrait soit (a) un flux OAuth "Web application" complet avec gestion de session par utilisateur, soit (b) — solution alignée avec le brief lui-même (section 8.1, étape 3) — remplacer la connexion live par un **import de fichier d'export Gmail (Google Takeout, `.mbox`)**, qui ne nécessite aucune vérification Google et fonctionne dès aujourd'hui pour n'importe qui. Cette seconde option a été identifiée mais pas implémentée par choix explicite de l'utilisateur pendant le hackathon.
