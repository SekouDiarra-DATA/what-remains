# Document Produit Exhaustif — Agent de Clôture Numérique Post-Mortem
## Version 2 — enrichie de données chiffrées et développée en profondeur

## Préambule : comment lire ce document

Ce document est délibérément long, dense et détaillé. Il ne contient aucune information technique — aucune mention de stack, d'API ou de code. Son unique objectif est de transmettre une compréhension complète, chiffrée et sans ambiguïté du projet, de sorte que toute personne le lisant (Claude Code, un coéquipier, un membre du jury) comprenne non seulement *ce que* fait le produit, mais *pourquoi* il existe, *pour qui*, à quelle échelle le problème se pose réellement, et avec quelle sensibilité il doit être construit. Chaque affirmation d'ampleur ou d'importance est, dans la mesure du possible, appuyée par un chiffre et sa source, plutôt que laissée à l'état d'impression générale.

Structure du document :
1. Contexte du projet et du hackathon
2. Le problème en profondeur, avec données chiffrées
3. Étude du marché existant, ses angles morts, et données chiffrées du secteur
4. Objectifs et non-objectifs
5. Utilisateurs cibles et personas détaillés
6. États émotionnels et psychologiques à anticiper
7. Scénarios d'usage détaillés
8. Parcours utilisateur complet, y compris cas limites
9. Considérations éthiques et légales
10. Ton, voix et posture du produit
11. Critères de succès et métriques
12. Risques, limites assumées et questions ouvertes
13. Annexe — récapitulatif chiffré complet avec sources
14. Glossaire complet

---

## 1. Contexte du projet et du hackathon

### 1.1 Le cadre général de l'événement
Ce projet est développé dans le cadre du hackathon mondial "Agents, Everywhere: Bots, Channels, & More", organisé par AI Tinkerers en partenariat avec Orange Digital Center Mali, le samedi 12 septembre 2026 à Bamako. Cet événement n'est pas un hackathon local isolé : il se déroule simultanément dans 49 villes à travers le monde, avec un seul et même processus d'évaluation mondial regroupant l'ensemble des projets soumis, quelle que soit la ville d'origine de l'équipe. Cette dimension mondiale a une conséquence directe et structurante sur la conception du produit : il doit être immédiatement compréhensible, pertinent et convaincant pour un jury qui ne connaît ni Bamako, ni le Mali, ni le contexte spécifique de l'équipe. Le problème choisi, et la façon dont on le présente, doivent donc parler à un public international par défaut, sans nécessiter d'explication culturelle préalable.

### 1.2 La consigne officielle du défi, et pourquoi elle structure tout le projet
Les organisateurs ont formulé le défi de la façon suivante : la plupart des agents conversationnels existants restent aujourd'hui enfermés dans une fenêtre de discussion séparée, déconnectée du reste de la vie numérique de la personne. Le défi de cette journée consiste précisément à sortir de ce cadre, en construisant un agent qui vit et opère à l'intérieur d'un outil, d'un canal, d'un appareil ou d'un environnement où les gens ont déjà une activité réelle : au travail (email, documents, calendriers, outils collaboratifs), dans leur poche (messagerie mobile), sur le web (navigateur), ou dans leur environnement physique (voix, objets connectés). L'agent doit tirer sa valeur du fait même d'être intégré dans ce contexte précis, et non simplement y être branché par commodité technique.

### 1.3 Pourquoi notre projet répond à cette consigne de façon particulièrement naturelle
Ce point mérite d'être développé, car il constitue un argument de vente central pour la présentation devant le jury. De nombreux projets d'agents IA choisissent un canal (Slack, WhatsApp, email) de façon presque interchangeable — l'idée pourrait fonctionner ailleurs sans perdre grand-chose. Ce n'est pas le cas ici : notre agent n'a de sens que parce qu'il opère directement sur le contenu réel d'une boîte email. Le canal n'est pas un choix d'implémentation parmi d'autres, il est constitutif du problème lui-même : c'est précisément parce que l'information nécessaire (quels comptes existent, quels abonnements sont actifs) est diluée et cachée dans des centaines d'emails que le problème existe. Un agent qui vivrait ailleurs ne pourrait tout simplement pas résoudre ce problème de la même manière.

### 1.4 Contraintes de production imposées par le format hackathon
Le cœur du projet doit être construit pendant la session de développement officielle, qui dure environ quatre heures et quart (de 11h15 à 15h30). Les équipes peuvent réutiliser des templates, des bibliothèques ou des briques de code déjà existantes, mais le projet soumis et sa fonctionnalité principale doivent être créés pendant l'événement lui-même — un projet préexistant ne peut pas être resoumis tel quel sous couvert de nouveauté. À la fin de cette session, chaque équipe doit produire cinq livrables obligatoires : un titre clair, une description écrite expliquant ce qui a été construit, pour qui, et pourquoi le contexte choisi compte réellement ; un dépôt GitHub public contenant du code fonctionnel et consultable ; une vidéo de démonstration de deux minutes maximum ; et un post public sur les réseaux sociaux mentionnant les sponsors et organisateurs de l'événement. Il n'existe pas de jugement local formel — seule la soumission finale, évaluée dans le pool mondial de tous les projets de toutes les villes, détermine le résultat.

### 1.5 Conséquence directe sur la conception du produit
Compte tenu du temps de développement extrêmement limité, le produit final présenté doit être un MVP volontairement circonscrit. Il vaut infiniment mieux démontrer un parcours complet, cohérent et convaincant sur un périmètre resserré (par exemple : la détection des abonnements et comptes financiers actifs à partir d'un jeu d'emails simulés) que de tenter de couvrir superficiellement l'intégralité du problème (toutes les plateformes possibles, tous les pays, tous les cas de figure). La qualité de l'exécution sur un périmètre restreint mais réel doit toujours primer sur l'ambition affichée d'un périmètre large mais fragile.

---

## 2. Le problème en profondeur, avec données chiffrées

### 2.1 Le constat de base, développé
Quand une personne meurt, il n'existe strictement aucun mécanisme automatique qui vienne clôturer, transférer ou signaler ses comptes numériques. Contrairement à l'intuition que l'on pourrait avoir dans un monde de plus en plus automatisé, rien ne se passe par défaut : l'adresse email continue de recevoir des messages, les prélèvements automatiques continuent de s'exécuter sur les comptes bancaires ou les cartes associées, les profils de réseaux sociaux restent visibles et actifs, et les documents stockés dans des services cloud restent accessibles ou non selon des règles qui varient d'une plateforme à l'autre, sans aucune coordination entre elles. Absolument rien ne bouge tant qu'un être humain ne prend pas l'initiative d'agir, service par service, un par un.

### 2.2 L'ampleur du problème en nombre de personnes concernées chaque année
Pour mesurer l'échelle réelle de ce problème, il faut d'abord regarder le nombre de décès dans le monde. Selon les estimations démographiques convergentes de plusieurs sources (Nations Unies, Our World in Data, StatisticsTimes), environ **63 à 64 millions de personnes meurent chaque année dans le monde** en 2026, soit environ **174 000 décès par jour**, ce qui représente environ **7 250 décès par heure**, ou encore **près de deux décès chaque seconde** sur la planète. Chacun de ces décès déclenche, dans la quasi-totalité des cas, exactement le même problème non résolu : une vie numérique entière qui continue d'exister sans supervision, jusqu'à ce qu'un proche s'en occupe manuellement. Ce chiffre à lui seul suffit à démontrer qu'il ne s'agit en aucun cas d'un problème de niche, mais d'un phénomène structurel touchant, à un moment ou un autre, la quasi-totalité des familles humaines sur Terre.

### 2.3 L'ampleur de la vie numérique moyenne d'une personne aujourd'hui
Le problème s'aggrave mécaniquement avec la numérisation croissante des existences individuelles. Plusieurs études convergent pour montrer que le nombre de comptes en ligne détenus par une personne moyenne a explosé ces dernières années :
- Une étude portant sur les habitudes numériques (données Version 2, reprises dans plusieurs analyses de sécurité en 2026) indique que la personne moyenne détient aujourd'hui **près de 170 comptes en ligne nécessitant un mot de passe**, contre environ 100 comptes il y a seulement quelques années — une progression rapide qui illustre l'accélération du problème plutôt que sa stabilité.
- Sur les seuls réseaux sociaux, un utilisateur moyen entretient environ **6,5 comptes actifs sur des plateformes différentes** chaque mois à l'échelle mondiale ; ce chiffre grimpe à environ 11 comptes en Inde, 7 aux États-Unis et au Royaume-Uni, contre environ 4 au Japon — ce qui illustre aussi une variabilité culturelle importante que le produit devra garder à l'esprit.
- Sur le plan des abonnements payants uniquement (streaming, logiciels, salles de sport, presse), les chiffres varient selon les méthodologies mais convergent vers un ordre de grandeur significatif : certaines études évoquent une moyenne de 3,4 abonnements payants actifs par personne aux États-Unis en 2026, tandis que d'autres études, incluant les abonnements moins visibles (applications mobiles, services groupés), évoquent une moyenne bien plus élevée, autour de 8 à 12 abonnements actifs par personne selon les sources.
- Le monde compte aujourd'hui environ **6,2 milliards d'internautes actifs**, ce qui signifie que la quasi-totalité des 63 millions de décès annuels concerne des personnes ayant laissé derrière elles une empreinte numérique substantielle, avec des dizaines, voire des centaines de comptes potentiellement actifs.

### 2.4 L'ampleur du problème en termes financiers directs
Le volet financier du problème est particulièrement documenté et chiffrable, même s'il concerne principalement des données disponibles pour les marchés occidentaux (ce qui constitue en soi un argument supplémentaire en faveur de notre angle différenciant, développé en partie 3) :
- Selon une étude de 2026 (Self Financial, portant sur plus de 1 270 adultes américains), environ **60 % des personnes ont au moins un abonnement payant qu'elles n'utilisent plus**, pour une valeur moyenne d'environ 27 dollars par mois de charges "oubliées".
- Une autre analyse (SubStop, 2026) évalue que les foyers américains gaspillent collectivement plus de **15,5 milliards de dollars par an** en abonnements oubliés ou non résiliés.
- Ces chiffres concernent des personnes vivantes qui oublient simplement de résilier — le problème est structurellement pire après un décès, puisque, par définition, la personne qui aurait pu remarquer et arrêter le prélèvement n'est plus en mesure de le faire, et que ses proches ignorent souvent purement et simplement l'existence de l'abonnement.
- Il faut ajouter à cela des pertes non récupérables : dans le cas de cryptomonnaies stockées dans un portefeuille personnel sans clé de sauvegarde connue de la famille, la perte est totale et définitive — aucune procédure, aucun service client, aucune décision de justice ne peut la contourner.

### 2.5 L'ampleur du problème en termes de préparation (ou plutôt d'absence de préparation)
C'est peut-être la donnée la plus importante pour justifier la nécessité d'un outil **réactif** (qui agit après le décès) plutôt que seulement préventif (qui aide à préparer sa succession numérique de son vivant) :
- Selon le rapport Trust & Will de 2026, **23 % des personnes ayant rédigé un testament classique n'ont laissé absolument aucune instruction concernant leurs comptes numériques**, et ce chiffre monte même à l'envers pour les détenteurs de trusts (11 % sans aucune instruction malgré une planification patrimoniale plus poussée par ailleurs).
- Plus largement, une étude distincte évoque que près de **48 % des personnes n'ont aucun plan concernant leurs comptes numériques après leur mort** — ce qui signifie que, dans près d'un cas sur deux, la famille se retrouve face à une situation totalement non préparée, sans aucun point de départ, sans liste, sans mot de passe transmis.
- Ce déficit de préparation touche même les personnes qui, par ailleurs, ont fait l'effort de planifier leur succession classique (testament, biens physiques) — ce qui démontre que le numérique reste un angle mort systématique de la planification successorale, quel que soit le sérieux avec lequel le reste de la succession a été préparé.

### 2.6 Le vrai goulot d'étranglement : ce n'est pas résilier, c'est découvrir
Un point revient de façon constante dans la quasi-totalité des guides pratiques destinés aux familles endeuillées : la difficulté principale n'est presque jamais de résilier un compte une fois qu'on en connaît l'existence — les procédures de résiliation, bien que parfois fastidieuses, sont documentées et suivables. La vraie difficulté, systématiquement citée en premier, est de **découvrir** que le compte existe. L'information nécessaire est diluée dans des centaines, parfois des milliers d'emails, de relevés bancaires et de notifications, qu'aucune personne en situation de deuil n'a l'énergie ni le temps de parcourir méthodiquement un par un. C'est précisément ce goulot d'étranglement — la découverte, pas la résiliation — que notre agent cible en priorité, car c'est là que l'automatisation apporte la valeur la plus immédiate et la plus démontrable.

### 2.7 Conséquences non financières, tout aussi réelles
Au-delà de l'aspect purement monétaire, plusieurs conséquences supplémentaires méritent d'être mentionnées pour la richesse du dossier :
- La perte potentielle et irréversible de souvenirs numériques (photos, vidéos) stockés uniquement dans un compte cloud personnel, si personne ne parvient à y accéder avant une suppression automatique liée à l'inactivité prolongée du compte
- La charge émotionnelle additionnelle causée par des rappels automatiques non désirés (notifications d'anniversaire sur les réseaux sociaux, emails promotionnels, suggestions algorithmiques) qui peuvent raviver la douleur du deuil de façon incontrôlée
- Le sentiment de culpabilité ou d'échec ressenti par les proches lorsqu'ils réalisent, parfois des mois plus tard, qu'ils ont "oublié" un compte ou laissé filer un prélèvement, alors même qu'ils ont fait de leur mieux dans une période de vulnérabilité maximale

---

## 3. Étude du marché existant, ses angles morts, et données chiffrées du secteur

### 3.1 Panorama détaillé des solutions existantes

**a) Les outils natifs proposés par les grandes plateformes technologiques**
Google, Facebook (Meta) et Apple proposent chacun, depuis plusieurs années, un mécanisme permettant à un utilisateur de désigner à l'avance, de son vivant, ce qu'il adviendra de son compte après son décès : un "gestionnaire de compte inactif" chez Google, un "contact légataire" chez Facebook, un "contact héritage" chez Apple. Ces outils sont fonctionnels et gratuits, mais ils partagent tous la même limite structurelle majeure : ils ne sont utiles que s'ils ont été activement configurés *avant* le décès. Or, comme démontré par les chiffres de la partie 2.5, c'est précisément ce qui manque dans près de la moitié des cas.

**b) Les startups spécialisées dans la planification successorale numérique**
Une catégorie d'acteurs commerciaux s'est développée pour accompagner la préparation de sa succession numérique : Elayne, CareTabs, Myend, Trust & Will, entre autres. Ces services permettent de lister ses comptes, de stocker des instructions, parfois de centraliser des mots de passe dans un coffre-fort numérique sécurisé. Certains proposent également des guides détaillés, plateforme par plateforme, pour accompagner une famille déjà en situation de deuil dans la résiliation manuelle de chaque service identifié. Le marché de la planification successorale numérique dans son ensemble est évalué à environ **22,5 milliards de dollars en 2024**, avec une projection de croissance vers environ **79 milliards de dollars d'ici 2034** — ce qui démontre à la fois l'ampleur économique du problème perçu et la marge de progression encore disponible sur ce marché.

**c) L'industrie du "grief tech" (technologies du deuil numérique et émotionnel)**
Un secteur en croissance rapide et distincte propose de recréer numériquement une version conversationnelle, vocale ou audiovisuelle de la personne décédée, à partir d'enregistrements réalisés de son vivant : HereAfter AI, StoryFile, Eternos, Seance AI, Project December en sont les représentants les plus connus. Ce secteur, souvent désigné sous le terme de "grief tech", est évalué à plus de **5 milliards de dollars en 2026**, avec une croissance continue anticipée.

### 3.2 Ce que ces trois catégories de solutions ne couvrent pas — l'angle mort identifié
En confrontant méthodiquement chacune de ces trois catégories au problème réel décrit en partie 2, un angle mort clair et documenté apparaît :

Un article d'analyse récent du secteur du "grief tech", publié en 2026, formule ce constat de façon particulièrement nette et directement citable dans notre argumentaire : l'essentiel de l'attention publique, de l'investissement et de l'innovation dans ce secteur se porte sur la simulation émotionnelle (cloner une voix, reconstituer une personnalité, permettre une conversation avec un avatar du défunt), alors que la partie strictement pratique et opérationnelle du problème — accéder effectivement aux comptes, identifier les abonnements encore actifs, localiser les documents financiers et légaux nécessaires — demeure très largement non résolue par ces mêmes acteurs. L'article souligne qu'aucune de ces technologies de simulation émotionnelle ne peut, par exemple, payer une mensualité de prêt à la place du défunt, résilier un abonnement, ou indiquer à la famille où se trouvent les documents d'assurance-vie.

Ce constat se double d'une seconde observation, tout aussi importante : même les solutions de la catégorie (b), qui s'attaquent bien à la partie pratique du problème, le font presque exclusivement par le biais de **checklists génériques et de formulaires statiques** que l'utilisateur doit dérouler manuellement, de mémoire, compte par compte. Aucune de ces solutions recensées n'analyse **activement et automatiquement** le contenu réel d'une boîte email pour découvrir, sans effort de mémoire de la part de l'utilisateur, quels comptes existent effectivement.

Enfin, une troisième observation structurelle mérite d'être soulignée : la quasi-totalité des solutions et des guides trouvés sont pensés pour un public anglophone et pour un cadre juridique nord-américain — le cadre légal RUFADAA (Revised Uniform Fiduciary Access to Digital Assets Act), adopté par la plupart des États américains, est cité comme référence structurante dans la majorité des ressources analysées. Cela rend ces solutions peu adaptées, voire simplement absentes, pour un public francophone ou pour des contextes juridiques différents, alors même que le problème sous-jacent — la vie numérique qui continue après la mort — est parfaitement universel, comme démontré par le chiffre de 63 millions de décès annuels dans le monde entier.

### 3.3 Notre positionnement différenciant, reformulé avec précision
Notre projet ne prétend pas résoudre un problème totalement inédit dans l'absolu — un tel problème n'existe quasiment plus dans le paysage saturé des agents IA en 2026. Ce qu'il propose, en revanche, est une **combinaison précise et vérifiablement absente du marché actuel** : (1) une analyse active et automatisée du contenu réel d'une boîte email, plutôt qu'une checklist générique statique à dérouler manuellement ; (2) une conception pensée dès le départ pour le moment *après* le décès, au service d'une famille déjà submergée, plutôt que pour la préparation préventive de son vivant ; et (3) une approche linguistiquement et culturellement adaptable à un public non-anglophone et non nécessairement soumis au cadre juridique américain. Cette combinaison précise constitue un vide de marché réel et vérifiable, même si chacun de ses trois éléments pris isolément existe déjà ailleurs sous une forme ou une autre.

---

## 4. Objectifs et non-objectifs

### 4.1 Objectif principal
Réduire de façon radicale et mesurable le temps, l'effort cognitif et la charge émotionnelle nécessaires pour qu'un proche identifie l'ensemble des comptes numériques actifs d'une personne décédée, en transformant une tâche manuelle potentiellement longue de plusieurs semaines et confuse en une analyse automatisée, claire et priorisée, réalisable en quelques minutes.

### 4.2 Objectifs secondaires, détaillés et hiérarchisés
1. **Éviter les pertes financières évitables** — chaque mois de retard dans la détection d'un abonnement actif représente, comme démontré en partie 2.4, une perte financière moyenne mesurable et documentée (de l'ordre de 27 dollars par mois et par abonnement oublié selon les études américaines de référence, un ordre de grandeur transposable conceptuellement à d'autres contextes économiques)
2. **Redonner un sentiment de maîtrise et de clarté** à une personne en situation de vulnérabilité maximale, plutôt que de la laisser submergée par une masse d'informations désorganisées et anxiogène
3. **Garantir explicitement, à chaque étape du parcours**, que l'outil ne prend jamais de décision irréversible à la place de l'être humain — ce principe est développé en détail en partie 9
4. **Produire un livrable concret, tangible et transférable** (une liste structurée, un document exportable), utile non seulement à l'utilisateur direct mais également à un tiers professionnel comme un notaire ou un exécuteur testamentaire

### 4.3 Non-objectifs — ce que ce produit ne cherche délibérément pas à être
Il est tout aussi important, sinon davantage, de définir précisément ce que ce produit ne fait pas, afin d'éviter toute dérive de conception pendant le développement, même sous la pression du temps :
- Il ne cherche à aucun moment à simuler, recréer ou faire "parler" numériquement la personne décédée, sous quelque forme que ce soit — ce positionnement le distingue explicitement et volontairement de tout le secteur du "grief tech" décrit en partie 3.1(c)
- Il n'envoie, ne résilie, ne modifie et ne supprime jamais un compte ou un service de façon autonome — toute action concrète et irréversible reste entièrement et systématiquement entre les mains de l'utilisateur humain
- Il ne fournit pas de conseil juridique, fiscal ou successoral au sens strict ; il ne remplace en aucun cas l'intervention d'un notaire, d'un avocat ou d'un exécuteur testamentaire qualifié
- Il ne couvre pas la gestion de la succession dans son ensemble (biens physiques, testament classique, partage entre héritiers) : son périmètre est strictement et volontairement limité à l'identification et à l'organisation des comptes et services numériques

---

## 5. Utilisateurs cibles et personas détaillés

### 5.1 Persona principal : le proche endeuillé désigné
**Profil démographique type** : un conjoint survivant, un enfant adulte, ou un frère/sœur proche, généralement âgé de 30 à 65 ans, qui se retrouve, souvent sans l'avoir choisi explicitement, responsable de facto de "s'occuper des affaires" du défunt — en plus de son propre deuil personnel et de ses obligations quotidiennes habituelles (travail, propre foyer, propres enfants).

**Rapport à la technologie** : très hétérogène au sein de cette population — certains membres de cette catégorie sont parfaitement à l'aise avec les outils numériques modernes, d'autres beaucoup moins, notamment parmi les générations plus âgées qui composent une part importante des conjoints survivants. Le produit doit impérativement être conçu pour être compris et utilisé sans compétence technique particulière, sous peine d'exclure une part significative de sa cible principale.

**Situation émotionnelle et cognitive détaillée** : fatigue physique et psychologique souvent déjà installée depuis plusieurs semaines si la maladie précédant le décès a été longue ; charge mentale déjà saturée par l'ensemble des démarches administratives classiques qui accompagnent un décès (déclaration officielle, organisation des obsèques, ouverture de la succession) ; capacité de concentration objectivement réduite dans ce contexte, ce qui rend toute tâche perçue comme complexe ou floue rapidement décourageante et source d'évitement.

**Ce que cette personne recherche fondamentalement, formulé avec précision** : ne pas avoir à réfléchir ni à apprendre quoi que ce soit de nouveau dans un moment où l'énergie mentale disponible est structurellement au plus bas ; obtenir une réponse simple et directe à la question implicite "qu'est-ce qu'il reste concrètement à faire, et dans quel ordre de priorité" ; avoir la certitude absolue qu'elle ne va pas "casser" quelque chose, perdre un accès important, ou commettre une erreur irréversible par méconnaissance des procédures.

### 5.2 Persona secondaire : le professionnel mandaté (notaire, exécuteur testamentaire, avocat en droit des successions)
**Profil type détaillé** : professionnel du droit ou de la gestion patrimoniale, mandaté légalement et formellement pour établir l'inventaire complet des actifs — y compris numériques — d'une personne décédée, dans le cadre d'une procédure de succession encadrée.

**Ce qui le distingue nettement du persona principal** : il aborde la tâche de façon professionnelle, méthodique et généralement détachée émotionnellement du défunt lui-même, mais il gère très fréquemment plusieurs dossiers de succession en parallèle, ce qui signifie que son critère de valeur principal est le gain de temps mesurable et la fiabilité du document produit, plutôt que le réconfort émotionnel recherché par le persona principal.

**Besoin spécifique et différenciant** : un export de résultat propre, formel, structuré, daté, et idéalement défendable en cas de contestation ultérieure par un héritier — plutôt qu'une simple interface conversationnelle informelle, qui conviendrait moins bien à un usage professionnel documenté.

### 5.3 Persona tertiaire (mentionné pour complétude, non prioritaire pour le MVP hackathon)
Une personne consciente de l'imminence de sa propre fin de vie (maladie en phase terminale diagnostiquée, par exemple) pourrait vouloir utiliser une version proactive et adaptée de l'outil, pour préparer elle-même, de son vivant, la liste de ses comptes actifs à l'attention de ses proches futurs. Ce cas d'usage est documenté ici par souci d'exhaustivité et de vision produit à long terme, mais il implique un ton, un parcours et des mécanismes de consentement fondamentalement différents (préparation autonome et consentie, plutôt que gestion après coup par un tiers), et ne doit en aucun cas être développé dans le cadre du MVP du hackathon, sous peine de disperser dangereusement l'effort de développement disponible.

---

## 6. États émotionnels et psychologiques à anticiper

Cette section est volontairement distincte de la description des personas eux-mêmes, car elle doit être gardée activement à l'esprit à chaque décision de contenu, de formulation et de parcours utilisateur, et pas seulement traitée une seule fois au moment de définir qui est l'utilisateur cible.

- **La culpabilité** : de nombreuses personnes ressentent un malaise diffus à l'idée de "s'occuper de choses matérielles" (abonnements, argent, comptes) dans les jours ou semaines suivant immédiatement la mort d'un proche ; le produit doit activement légitimer cette démarche comme un acte de soin et de protection de la famille, et non comme une préoccupation mesquine ou déplacée
- **La peur de l'erreur irréversible** : la crainte de supprimer, résilier, ou perdre par erreur quelque chose d'important (des photos, un accès, une information) peut littéralement paralyser l'utilisateur au moment d'agir ; chaque action proposée par l'outil doit donc être clairement présentée comme réversible, ou clairement identifiée comme nécessitant une validation explicite avant toute exécution
- **L'épuisement décisionnel accumulé** : après des semaines, parfois des mois, de démarches administratives diverses, la capacité même à prendre des décisions simples diminue objectivement ; le produit doit donc systématiquement proposer des choix par défaut clairs et raisonnables, plutôt que de multiplier les options et les paramètres à considérer
- **Le besoin de reconnaissance explicite de la difficulté du moment** : un ton qui ignorerait complètement le contexte émotionnel sous-jacent (trop froid, trop corporate, ou à l'inverse trop enjoué ou familier) serait perçu comme profondément déplacé et pourrait durablement nuire à la confiance de l'utilisateur envers l'outil, voire le pousser à l'abandonner en cours de route
- **La variabilité individuelle du rythme d'usage** : certaines personnes voudront traiter l'intégralité du sujet en une seule session pour "en finir" au plus vite, tandis que d'autres auront besoin, structurellement, de faire des pauses sur plusieurs jours voire plusieurs semaines ; le produit doit accommoder les deux approches sans porter de jugement implicite sur l'une ou l'autre

---

## 7. Scénarios d'usage détaillés

### Scénario A — Décès soudain et totalement inattendu
Une personne décède subitement (accident de la route, crise cardiaque, autre cause brutale) sans avoir rien préparé ni documenté au préalable concernant sa vie numérique. La famille découvre, souvent avec un sentiment de sidération, l'ampleur réelle de la vie numérique du défunt, sans aucun point de départ ni aucune liste préexistante, avec un sentiment simultané de submersion et d'urgence (notamment la peur légitime que des prélèvements bancaires automatiques continuent de s'exécuter). C'est le scénario dans lequel l'outil apporte la valeur la plus immédiate, la plus tangible et la plus démontrable pour une présentation de hackathon.

### Scénario B — Décès survenant après une maladie longue et anticipée
Dans ce cas, la famille a généralement eu le temps de se préparer, au moins partiellement, sur le plan psychologique et parfois même administratif. Mais l'épuisement physique et émotionnel accumulé pendant toute la durée de la maladie (souvent des mois de soins, de visites, de gestion médicale) rend la charge administrative supplémentaire qui survient après le décès d'autant plus difficile à affronter, précisément parce que les réserves d'énergie de la famille sont déjà largement entamées. L'outil doit ici être perçu explicitement comme un soulagement bienvenu plutôt que comme une tâche de plus à accomplir.

### Scénario C — Décès d'un parent âgé, avec des enfants adultes dispersés géographiquement
Plusieurs enfants adultes, potentiellement situés dans des villes ou des pays différents (un cas de plus en plus fréquent avec la mobilité géographique croissante des familles contemporaines), doivent se coordonner à distance pour gérer la succession numérique du parent décédé. L'outil doit, au moins dans sa conception d'ensemble, permettre de partager facilement le résultat de l'analyse (la liste, l'export) entre plusieurs personnes qui ne peuvent pas nécessairement se réunir physiquement au même endroit au même moment.

### Scénario D — Intervention d'un professionnel mandaté dans un cadre légal formel
Un notaire ou un exécuteur testamentaire reçoit un mandat officiel d'exécution et doit produire, dans un cadre légal contraignant, un inventaire numérique formel et défendable des actifs numériques du défunt. Ce scénario, bien que secondaire pour le MVP du hackathon, doit rester conceptuellement cohérent avec l'architecture générale du produit : le même moteur d'analyse sous-jacent peut servir les deux types d'usage (familial et professionnel), seul le format de l'export final diffère significativement entre les deux publics.

### Scénario E — Contexte culturel où les mécanismes préventifs occidentaux sont peu connus ou peu utilisés
Dans certains contextes géographiques et culturels, notamment dans des pays où l'usage préventif des grandes plateformes américaines (Google Legacy Contact, Facebook Legacy Contact) est beaucoup moins ancré dans les habitudes de préparation successorale qu'aux États-Unis ou en Europe occidentale, la famille endeuillée n'a souvent même pas connaissance de l'existence de ces mécanismes préventifs, et n'aurait de toute façon pas pu les activer puisque le défunt ne les avait pas configurés de son vivant. L'outil, en étant conçu comme fondamentalement réactif plutôt que préventif, conserve toute sa pertinence et son utilité indépendamment de ce niveau de préparation préalable — ce qui renforce considérablement sa pertinence pour un public véritablement mondial, et pas seulement pour un public occidental déjà familiarisé avec ces outils natifs de plateforme.

---

## 8. Parcours utilisateur complet, y compris cas limites

### 8.1 Parcours nominal détaillé, étape par étape
1. **Arrivée sur l'outil** — L'utilisateur, souvent orienté vers l'outil par un proche, une recherche en ligne active, ou la recommandation d'un professionnel, découvre l'outil précisément au moment où il cherche activement une solution à ce problème concret et pressant
2. **Écran d'explication et de consentement explicite** — Avant toute chose et sans exception, l'outil doit expliquer en langage simple et accessible ce qu'il va faire concrètement, ce qu'il ne fera jamais sous aucun prétexte, et pourquoi cette autorisation d'accès est nécessaire ; ce moment précis est absolument critique pour établir une relation de confiance dès le premier contact
3. **Connexion à la source de données** — L'utilisateur relie la boîte email concernée par un mécanisme d'autorisation standard, ou importe une archive exportée si un accès direct n'est pas possible, pas souhaité, ou pas encore autorisé légalement
4. **Phase d'analyse automatisée** — Pendant que l'outil traite les données disponibles, l'attente doit être rendue explicite, transparente et rassurante par une indication claire de progression, plutôt que de laisser l'utilisateur face à un silence anxiogène sans information sur ce qui se passe
5. **Présentation structurée des résultats** — Une liste claire, hiérarchisée par ordre d'urgence décroissante, immédiatement compréhensible sans effort de lecture ou d'interprétation supplémentaire de la part de l'utilisateur
6. **Approfondissement optionnel élément par élément** — L'utilisateur peut, s'il le souhaite, cliquer sur un élément spécifique de la liste pour obtenir davantage de détails contextuels ou un brouillon d'action concret associé à cet élément précis
7. **Action assistée mais jamais autonome** — Génération, sur demande explicite, d'un brouillon de communication ou de résiliation, qui n'est jamais envoyé automatiquement par le système, et que l'utilisateur peut librement modifier avant de l'envoyer lui-même par ses propres moyens habituels
8. **Export et clôture de session** — Possibilité claire de sauvegarder ou d'exporter la liste complète des résultats, de revenir ultérieurement reprendre le travail là où il avait été interrompu, ou de la partager directement avec d'autres membres de la famille impliqués dans la démarche

### 8.2 Cas limite — Aucun compte détecté, ou résultat d'analyse très pauvre
Si l'analyse automatisée ne parvient à identifier que peu, voire aucun élément véritablement exploitable (par exemple parce que la boîte email analysée était peu utilisée par le défunt de son vivant, était relativement ancienne, ou se situe simplement hors du périmètre effectivement analysable par l'outil), celui-ci doit impérativement le communiquer de façon honnête et transparente à l'utilisateur, plutôt que de forcer artificiellement une liste peu fiable pour donner une impression de succès. Dans ce cas, l'outil doit également suggérer des pistes complémentaires raisonnables (vérifier une autre adresse email potentiellement utilisée, consulter directement un relevé bancaire récent, etc.).

### 8.3 Cas limite — Classification incertaine d'un élément détecté
Certains expéditeurs ou comptes détectés dans les emails peuvent rester ambigus par nature : un email publicitaire ponctuel envoyé une seule fois n'est pas nécessairement la preuve d'un compte actif et récurrent. L'outil doit distinguer clairement et visuellement, dans sa présentation des résultats, ce dont il est raisonnablement certain de ce qui reste incertain ou à vérifier manuellement, plutôt que de présenter une liste uniformément affirmative qui donnerait à l'utilisateur une fausse impression de fiabilité totale et risquerait de générer une confiance excessive et mal placée dans le résultat.

### 8.4 Cas limite — L'utilisateur interrompt puis reprend sa session ultérieurement
Étant donné la charge émotionnelle particulièrement lourde du contexte d'usage, il est hautement probable que l'utilisateur ne traite pas l'ensemble de la tâche en une seule session continue. Le parcours doit donc impérativement prévoir la possibilité technique et conceptuelle de reprendre un travail déjà partiellement commencé, sans avoir à tout recommencer depuis le début, ce qui serait à la fois frustrant et décourageant dans ce contexte précis.

### 8.5 Cas limite — Plusieurs membres de la famille sont impliqués simultanément
Il est fréquent, comme évoqué dans le scénario C de la partie 7, que plusieurs personnes différentes (le conjoint survivant, plusieurs enfants adultes) souhaitent consulter, compléter ou valider ensemble la même analyse. Le produit doit, au minimum sur le plan conceptuel, envisager sérieusement un mode de partage cohérent du résultat final, même si son implémentation technique complète dépasse très probablement le cadre temporel restreint du MVP développé pendant le hackathon.

---

## 9. Considérations éthiques et légales

### 9.1 Principe fondamental et non négociable : l'humain décide toujours
Aucune action irréversible — envoi effectif d'un email de résiliation, suppression d'un compte, modification de paramètres, transfert de quelque nature que ce soit — n'est jamais exécutée automatiquement par l'agent, en aucune circonstance. L'agent recherche, analyse, classe et propose des actions ; l'être humain valide consciemment, puis exécute lui-même. Ce principe ne constitue pas seulement une précaution technique parmi d'autres : il est au cœur même de la proposition de valeur éthique et de la confiance que le produit cherche à établir avec des utilisateurs en situation de grande vulnérabilité émotionnelle.

### 9.2 Consentement et légitimité de l'accès à la boîte email
L'outil doit systématiquement partir du principe que l'accès fourni à la boîte email est légitime — qu'il résulte d'un accès hérité légalement, d'un mandat formel, ou d'une autorisation familiale explicite — sans pour autant chercher à vérifier ou à juger lui-même cette légitimité de façon autonome. Cette responsabilité reste entièrement du ressort de l'utilisateur humain qui initie la démarche, exactement comme c'est déjà le cas aujourd'hui pour n'importe quel accès manuel à un compte de personne décédée, indépendamment de l'outil utilisé.

### 9.3 Confidentialité et sensibilité extrême des données traitées
Le contenu d'une boîte email représente une donnée personnelle et sensible par nature, et cette sensibilité est encore renforcée lorsqu'il s'agit de la boîte email d'une personne décédée, qui ne peut évidemment plus consentir elle-même, en temps réel, au traitement effectué sur ses données. Le produit doit donc, aussi bien dans son discours explicite que dans sa conception technique sous-jacente, traiter cette donnée avec le niveau de précaution le plus élevé possible, et ne jamais donner l'impression de "fouiller" au-delà de ce qui est strictement nécessaire à l'objectif fonctionnel poursuivi — à savoir l'identification de comptes actifs, et non la lecture ou l'exploitation de correspondances personnelles ou intimes qui ne concernent en rien l'objectif du produit.

### 9.4 Absence stricte de conseil juridique
Le produit ne doit à aucun moment formuler ses recommandations sous une forme qui pourrait être perçue comme un conseil juridique ferme ou une obligation légale impérative ("vous devez impérativement faire ceci"), mais toujours sous la forme d'une suggestion pratique et mesurée ("il est généralement recommandé de faire ceci ; vérifiez auprès d'un professionnel qualifié en cas de doute ou de situation particulière").

### 9.5 Variabilité importante des cadres légaux selon les pays
Le produit doit rester pleinement conscient que les règles concernant l'accès légal aux comptes numériques d'une personne décédée varient considérablement d'un pays à l'autre — certains pays disposent de cadres légaux spécifiquement dédiés à cette question (comme le RUFADAA mentionné en partie 3.2 pour la plupart des États américains), tandis que de nombreux autres pays n'ont, à ce jour, aucun cadre légal comparable. Le produit ne doit donc jamais affirmer une règle légale universelle valable partout, mais rester systématiquement au niveau de la bonne pratique générale et inviter explicitement à la vérification locale auprès d'un professionnel compétent.

---

## 10. Ton, voix et posture du produit

### 10.1 Principes directeurs fondamentaux
- **La sobriété avant toute chose** : aucun humour, aucune familiarité excessive, aucune formulation exagérément enjouée ou commercialement enthousiaste
- **La clarté sans jamais tomber dans la froideur** : des phrases simples, directes et faciles à comprendre rapidement, mais jamais cliniques, administratives ou impersonnelles à l'excès
- **La réassurance active et répétée tout au long du parcours** : rappeler à plusieurs moments clés du parcours — pas uniquement au tout début — que rien d'irréversible ne se produit jamais sans une validation explicite de l'utilisateur
- **Le respect scrupuleux du rythme propre à chaque utilisateur** : ne jamais donner l'impression de presser ou de bousculer l'utilisateur, ni de minimiser implicitement la difficulté réelle de la tâche qu'il est en train d'accomplir

### 10.2 Exemples concrets de formulations à privilégier, en opposition à celles à éviter absolument
- À privilégier : *"Voici ce que nous avons trouvé à partir des emails analysés. Rien n'a été envoyé ni modifié à ce stade — c'est entièrement à vous de décider de la suite, à votre propre rythme."*
- À éviter absolument : *"Analyse terminée ! 12 comptes trouvés, cliquez ici pour tout résilier en un seul clic !"*
- À privilégier : *"Nous ne sommes pas entièrement certains pour cet élément précis — nous vous recommandons de le vérifier vous-même avant d'entreprendre toute action."*
- À éviter absolument : toute présentation qui donnerait une fausse impression d'exhaustivité ou de certitude absolue sur des résultats qui, par nature, comportent une marge d'incertitude

### 10.3 Adaptation linguistique et culturelle du ton
Le ton général doit rester adaptable à différentes langues et à différents contextes culturels sans jamais perdre sa sobriété fondamentale — l'un des angles différenciants centraux du produit étant justement de ne pas être conçu exclusivement pour un public anglophone et occidental, contrairement à la quasi-totalité des solutions concurrentes recensées en partie 3.

---

## 11. Critères de succès et métriques, dans le contexte spécifique du hackathon

### 11.1 Critères de succès attendus pour la démonstration finale
- L'agent doit démontrer concrètement, à partir d'un jeu de données email réaliste (réel ou simulé pour des raisons évidentes de confidentialité), sa capacité effective à identifier des comptes actifs de façon crédible et à les présenter de façon claire, structurée et priorisée
- Au moins un exemple concret et pleinement convaincant de brouillon d'action généré par l'agent doit être montré explicitement pendant la démonstration
- La démonstration doit raconter une histoire narrative complète et cohérente : partir du problème humain réel et documenté (la famille dépassée face à une boîte email inconnue), montrer l'agent à l'œuvre de façon fluide et naturelle, et arriver à un résultat concret, clair et rassurant pour l'utilisateur
- Le projet doit illustrer sans la moindre ambiguïté le critère central du défi du hackathon : un agent qui vit et agit véritablement dans un outil du quotidien (l'email), et non un simple chatbot isolé répondant à des questions dans une fenêtre séparée

### 11.2 Ce qui ferait objectivement échouer la démonstration, à éviter absolument
- Une démonstration qui se limiterait à montrer un chatbot conversationnel répondant à des questions générales, sans jamais montrer d'analyse concrète ni d'action réelle sur des données effectives
- Un ton ou des choix visuels manifestement inadaptés à la sensibilité intrinsèque du sujet traité (trop ludiques, trop commerciaux, trop "startup enthousiaste")
- L'absence de mention claire et explicite, pendant la présentation, du principe fondamental de non-automatisation des actions irréversibles — qui constitue pourtant un argument de différenciation important et facilement compréhensible devant le jury

---

## 12. Risques, limites assumées et questions ouvertes

### 12.1 Risques identifiés à anticiper
- **Le risque de faux positifs ou de faux négatifs dans la classification automatisée** : l'agent peut légitimement se tromper en identifiant un compte comme actif alors qu'il ne l'est en réalité plus, ou inversement en manquant un compte réellement actif ; ce risque inhérent doit être communiqué honnêtement et clairement à l'utilisateur, plutôt que d'être dissimulé derrière une présentation faussement rassurante
- **Le risque de perception intrusive de la démarche** : même dans le cadre d'un accès parfaitement légitime, l'idée qu'une intelligence artificielle "lise" et analyse les emails personnels d'une personne décédée peut légitimement susciter un malaise psychologique chez l'utilisateur ; le discours global du produit doit anticiper activement ce malaise et chercher à le désamorcer par la transparence
- **Le risque de sur-promesse fonctionnelle** : présenter l'outil comme une solution complète, exhaustive et infaillible à l'intégralité de la gestion d'une succession numérique serait à la fois factuellement inexact et éthiquement problématique au vu de la sensibilité du sujet traité

### 12.2 Limites assumées explicitement pour la version développée pendant le hackathon (MVP)
- Le MVP n'a pas vocation à couvrir l'intégralité des plateformes numériques existantes dans le monde, ni l'ensemble des cadres juridiques nationaux applicables
- Le MVP n'a pas vocation à gérer nativement, dans sa version de démonstration, le partage entre plusieurs membres différents d'une même famille, même si le concept global doit rester pleinement compatible avec cette évolution future
- Le MVP peut légitimement s'appuyer sur des données entièrement simulées pour les besoins de la démonstration, plutôt que sur une véritable boîte email de personne décédée, pour des raisons évidentes et incontournables de disponibilité des données et de confidentialité

### 12.3 Questions ouvertes restant à trancher avant ou pendant le développement
- Quel est le nom final retenu pour le produit, et quelle tonalité précise ce nom doit-il transmettre dès la première impression ?
- Le produit doit-il, dans sa version démontrée devant le jury, se positionner explicitement et uniquement pour le persona "famille endeuillée", ou doit-il plutôt chercher à démontrer sa compatibilité conceptuelle avec les deux personas principaux (famille et professionnel mandaté) sans pour autant se disperser dans l'exécution ?
- Jusqu'à quel niveau de granularité la classification par urgence des comptes détectés doit-elle aller pour rester à la fois crédible et facilement démontrable dans le cadre contraint d'une présentation de seulement deux minutes ?

---

## 13. Annexe — récapitulatif chiffré complet, avec sources

Cette annexe rassemble, en un seul endroit consultable rapidement, l'ensemble des chiffres cités dans ce document, pour faciliter leur réutilisation directe dans la description écrite de soumission, le script du pitch oral, ou tout support visuel préparé pour la présentation.

| Chiffre | Signification | Source citée dans ce document |
|---|---|---|
| ~63 à 64 millions | Décès dans le monde chaque année (2026) | Estimations convergentes ONU / Our World in Data / StatisticsTimes |
| ~174 000 | Décès par jour dans le monde | Idem |
| ~2 | Décès chaque seconde dans le monde | Idem |
| ~170 | Nombre moyen de comptes en ligne détenus par une personne aujourd'hui (contre ~100 il y a quelques années) | Données Version 2, reprises dans analyses de sécurité 2026 |
| ~6,5 | Nombre moyen de comptes de réseaux sociaux actifs par utilisateur et par mois dans le monde (jusqu'à 11 en Inde, 7 aux USA/UK) | Priori Data, 2026 |
| 6,2 milliards | Nombre d'internautes actifs dans le monde en 2026 | Siteefy, 2026 |
| ~60 % | Part des personnes ayant au moins un abonnement payant inutilisé chaque mois | Self Financial, étude 2026 (1 272 adultes américains) |
| ~27 dollars/mois | Valeur moyenne des abonnements "oubliés" par personne | Self Financial, 2026 |
| 15,5 milliards de dollars/an | Gaspillage collectif annuel estimé sur les abonnements oubliés (échelle américaine) | SubStop, 2026 |
| 23 % | Part des personnes ayant un testament mais aucune instruction numérique | Rapport Trust & Will, 2026 |
| 11 % | Part des détenteurs de trusts sans aucune instruction numérique | Rapport Trust & Will, 2026 |
| ~48 % | Part des personnes sans aucun plan pour leurs comptes numériques après leur mort | Étude citée par blog.afteryou.me, 2026 |
| 22,5 milliards de dollars (2024) → 79 milliards (2034 projeté) | Taille du marché de la planification successorale numérique | Trustbourne / blog.afteryou.me, 2026 |
| > 5 milliards de dollars (2026) | Taille du marché du "grief tech" (simulation émotionnelle post-mortem) | Analyse sectorielle citée, 2026 |

**Note de prudence méthodologique, à conserver pour l'honnêteté du dossier** : ces chiffres proviennent de sources et de méthodologies diverses (enquêtes déclaratives, projections démographiques, rapports sectoriels commerciaux), portant majoritairement sur le marché américain pour les données financières et comportementales. Ils doivent être présentés comme des ordres de grandeur illustratifs et convergents plutôt que comme des statistiques uniques, officielles et incontestables. Cette nuance elle-même peut être mentionnée avec profit devant un jury exigeant, comme preuve de rigueur plutôt que comme faiblesse de l'argumentaire.

---

## 14. Glossaire complet

- **Compte actif détecté** : tout service pour lequel l'agent a trouvé, dans les emails effectivement analysés, une preuve raisonnable d'utilisation récente ou récurrente (une facture, une confirmation d'inscription, un renouvellement, une alerte de paiement)
- **Action assistée** : toute action proposée ou préparée par l'agent (par exemple, la génération d'un brouillon de message) mais nécessitant systématiquement et sans exception une validation puis une exécution humaines explicites
- **Checklist priorisée** : le livrable principal présenté à l'utilisateur, organisant l'ensemble des comptes détectés par ordre décroissant d'urgence plutôt que par simple ordre alphabétique ou chronologique
- **Persona principal / secondaire / tertiaire** : catégories distinctes d'utilisateurs définies en détail en partie 5, utilisées pour orienter systématiquement les décisions de contenu et de parcours tout au long du développement
- **MVP (produit minimum viable)** : dans le contexte spécifique de ce document, la version volontairement restreinte du produit, réalisable dans le temps contraint du hackathon, qui démontre un parcours complet et convaincant sur un périmètre resserré plutôt qu'un périmètre large mais nécessairement superficiel
- **Grief tech** : secteur industriel désignant l'ensemble des produits centrés sur la simulation émotionnelle ou conversationnelle d'une personne décédée, par opposition à la gestion pratique et opérationnelle de ses affaires numériques, qui constitue le périmètre exclusif de notre propre projet
- **RUFADAA** : cadre légal américain (Revised Uniform Fiduciary Access to Digital Assets Act) régissant l'accès des exécuteurs testamentaires aux actifs numériques d'une personne décédée, adopté par la majorité des États américains, et mentionné ici uniquement à titre de repère comparatif pour souligner l'absence d'équivalent dans de nombreux autres pays
