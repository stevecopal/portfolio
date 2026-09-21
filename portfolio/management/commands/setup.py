from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import (
    Profile,
    SocialLink,
    Service,
    ServiceFeature,
    Experience,
    Project,
    ProjectImage,
    Technology,
    Testimonial,
    SiteSettings,
    SEO,
    Tool,
)


class Command(BaseCommand):
    help = "Seeds the portfolio with initial data"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding portfolio data..."))

        self.clear_existing_data()

        self.create_profile()
        self.create_social_links()
        self.create_site_settings()
        services = self.create_services()
        self.create_service_features(services)
        self.create_experiences()
        technologies = self.create_technologies()
        projects = self.create_projects(technologies)
        self.create_project_images(projects)
        self.create_testimonials()
        self.create_seo()
        self.create_tools()

        self.stdout.write(self.style.SUCCESS("Successfully seeded portfolio data!"))

    def clear_existing_data(self):
        models = [
            Profile,
            SocialLink,
            Service,
            ServiceFeature,
            Experience,
            Project,
            ProjectImage,
            Technology,
            Testimonial,
            SiteSettings,
            SEO,
            Tool,
        ]
        for model in models:
            model.objects.all().delete()

    def create_profile(self):
        return Profile.objects.create(
            full_name="Copal Satcheme",
            professional_name="Copal Satcheme",
            professional_title="Developpeur Full-Stack & Architecte de Solutions Digitales",
            short_bio="Je concois et developpe des solutions digitales modernes, performantes et orientees utilisateur pouraccelerer la croissance de votre entreprise.",
            biography="""
Je suis un Developpeur Full-Stack passionne, base a Bafoussam au Cameroun, avec une solide expertise dans la conception et le developpement d'applications web modernes. Je me specialise dans Django, Python, PostgreSQL et les technologies frontend comme Tailwind CSS et JavaScript.

Ma philosophie est simple : je commence par comprendre vos besoins, analyser votre problematique, puis construire une solution qui fonctionne reellement. La technologie doit servir les gens, pas l'inverse.

Chaque projet que je prends en charge beneficie de toute mon attention. J'ecris du code propre, maintenable et je livre des solutions conçues pour durer. Que vous ayez besoin d'une application web complete, d'une API sur mesure, d'un site vitrine professionnel ou de conseils techniques, je suis la pour vous accompagner.

Ce qui me distingue, c'est mon engagement envers la qualite et la satisfaction client. Je ne me contente pas de livrer un produit : je m'assure qu'il resout vraiment votre problematique et qu'il evolue avec vos besoins. Mes clients reviennent toujours, et c'est la meilleure preuve de mon travail.
            """,
            location="Bafoussam",
            country="Cameroon",
            city="Bafoussam",
            email="copalmr@gmail.com",
            phone="+237 699 274 423",
            whatsapp="+237 699 274 423",
            availability_status=True,
            availability_message="Disponible pour de nouveaux projets",
        )

    def create_social_links(self):
        social_links = [
            {
                "name": "GitHub",
                "platform": "github",
                "url": "https://github.com/stevecopal",
                "icon": "fab fa-github",
                "display_order": 1,
            },
            {
                "name": "WhatsApp",
                "platform": "whatsapp",
                "url": "https://wa.me/237699274423",
                "icon": "fab fa-whatsapp",
                "display_order": 2,
            },
            {
                "name": "Email",
                "platform": "email",
                "url": "mailto:copalmr@gmail.com",
                "icon": "fas fa-envelope",
                "display_order": 3,
            },
        ]
        for link in social_links:
            SocialLink.objects.create(**link)

    def create_site_settings(self):
        return SiteSettings.objects.create(
            site_name="Copal Satcheme | Portfolio",
            slogan="Des Solutions Digitales Qui Fonctionnent Vraiment",
            short_description="Developpeur Full-Stack & Architecte de Solutions Digitales",
            footer_text="Transformer vos idees en realite grace au code",
            copyright_text="© 2026 Copal Satcheme. Tous droits reserves.",
            primary_email="copalmr@gmail.com",
            year=2026,
            is_active=True,
            maintenance_mode=False,
        )

    def create_services(self):
        services_data = [
            {
                "title": "Developpement d'Applications Web",
                "slug": "developpement-applications-web",
                "short_description": "Applications web sur mesure, modernes et performantes, concues pour repondre exactement a vos besoins metier.",
                "description": """
Je concois et developpe des applications web completes, responsives et evolutives en utilisant des technologies modernes comme Django, Python, PostgreSQL pour le backend, et Tailwind CSS, JavaScript pour des interfaces utilisateur fluides et professionnelles.

Ce que je propose dans ce service :
- Applications web sur mesure avec Django et Python
- Sites vitrines professionnels et Landing Pages
- Applications SaaS et plateformes en ligne
- Systemes de gestion (CRM, ERP, gestion de projets)
- Design responsive qui s'adapte a tous les appareils
- Systemes d'authentification securises et gestion des utilisateurs
- Base de donnees optimisees et performantes
- Deploiement et hebergement configure

Chaque projet commence par une phase de decouverte approfondie. Je ne crois pas aux solutions pretes a l'emploi. Votre application sera concue specifiquement pour votre cas d'utilisation, avec une architecture solide qui permettra a votre entreprise de grandir.

Ce qui me rend different : je ne me contente pas de coder. Je comprends votre business, vos objectifs, et je construis une solution qui vous aide reellement a les atteindre. Chaque ligne de code a un but, chaque fonctionnalite a une raison d'etre.
                """,
                "icon": "fas fa-code",
                "hero_description": "Je developpe des applications web sur mesure qui sont rapides, securisees et evolutives. De simples sites vitrines aux plateformes complexes d'entreprise.",
                "problem": "Beaucoup d'entreprises souffrent de logiciels generiques qui ne correspondent pas exactement a leurs besoins. Elles perdent du temps et de l'argent a adapter leurs processus a des outils rigides qui ne sont pas faits pour elles.",
                "audience": "Entreprises ayant besoin d'applications web personnalisees, startups qui veulent lancer leur MVP, societes cherchant a digitaliser leurs operations, commerces en ligne et organisations qui veulent moderniser leur presence numerique.",
                "features": "Developpement sur mesure, design responsive, authentification securisee, fonctionnalites en temps reel, integration d'API, optimisation des performances, support technique continu.",
                "how_it_works": "Nous demarrons par un appel de decouverte pour comprendre vos besoins en profondeur. Ensuite, je conçois la solution, je la developpe en sprints iteratifs avec des points reguliers, et je la deploie une fois que vous etes entierement satisfait du resultat.",
                "benefits": "Une solution construite specifiquement pour vos besoins, du code moderne et maintenable, une architecture evolutive qui grandit avec vous, et un accompagnement dedie tout au long du projet et apres la livraison.",
                "included": "Code source complet, documentation technique detaillee, assistance au deploiement, formation a l'utilisation, et 30 jours de support gratuit apres le lancement.",
                "is_featured": True,
                "is_active": True,
                "display_order": 1,
            },
            {
                "title": "Conseil & Strategie Digitale",
                "slug": "conseil-strategie-digitale",
                "short_description": "Accompagnement expert pour vos choix technologiques, l'architecture de vos projets et l'optimisation de votre presence numerique.",
                "description": """
Vous avez un projet digital mais vous ne savez pas par ou commencer ? Vous avez des doutes sur le choix des technologies, l'architecture de votre application ou la strategie a adopter ? Je vous accompagne pour prendre les bonnes decisions des le depart.

Mes services de conseil incluent :
- Audit de votre situation numerique actuelle
- Etude de faisabilite technique pour vos projets
- Choix des technologies adaptees a votre budget et vos objectifs
- conception d'architecture technique optimisee
- Strategie de transformation digitale
- Optimisation des processus existants
- Recommandations pour ameliorer votre productivite
- Plan de developpement progressif et realiste

Faire les mauvais choix techniques des le debut peut vous couter des mois de travail et des milliers de francs CFA. Un regard experimente peut vous eviter des erreurs couteuses et vous orienter vers des solutions qui marchent vraiment.

Je ne me contente pas de donner des conseils generiques. J'analyse votre situation specifique, je comprends vos contraintes (budget, delais, equipe), et je propose des recommandations concretes et applicables immediatement. Vous repartez avec un plan d'action clair et realiste.

Mon objectif est simple : vous aider a construire sur des fondations solides pour que votre projet reussisse.
                """,
                "icon": "fas fa-lightbulb",
                "hero_description": "Obtenez des conseils d'expert pour vos defis techniques et strategiques. Je vous aide a faire les bons choix pour votre projet.",
                "problem": "Prendre les mauvaises decisions techniques des le debut peut entrainer des mois de retard, des depassements de budget considerables, et parfois meme l'echec du projet. Sans expertise technique, il est facile de se perdre dans les options disponibles.",
                "audience": "Startups qui planifient leur stack technique, equipes enfrentant des defis d'architecture, entreprises qui evaluent leur dette technique, dirigeants qui veulent digitaliser leur activite sans risque, et organisations qui cherchent a optimiser leurs outils existants.",
                "features": "Audit technique complet, recommandations personnalisees, etude de faisabilite, plan de migration, optimisation des performances, formation de vos equipes.",
                "how_it_works": "J'analyse votre setup actuel, j'identifie les problemes et les opportunites, je propose des solutions adaptees a votre contexte, et je fournis un rapport detaille avec des recommandations actionnables et un plan de mise en oeuvre.",
                "benefits": "Evitez les erreurs couteuses, optimisez votre processus de developpement, construisez une base solide pour la croissance, et gagnez du temps et de l'argent en faisant les bons choix des le depart.",
                "included": "Rapport d'analyse detaille, document de recommandations, plan d'action priorise, et session de suivi pour repondre a vos questions.",
                "is_featured": True,
                "is_active": True,
                "display_order": 2,
            },
            {
                "title": "Integration d'API & Systemes",
                "slug": "integration-api-systemes",
                "short_description": "Connexion de vos applications et systemes pour un flux de donnees fluide et automatique entre tous vos outils.",
                "description": """
Vos logiciels ne communiquent pas entre eux ? Vous passez des heures a transferer des donnees manuellement d'un outil a un autre ? Je conçois et developpe des API et des integrations qui connectent vos systemes et automatisent vos flux de travail.

Mes services d'integration incluent :
- Conception et developpement d'API RESTful sur mesure
- Integration avec les API tierces (Mobile Money, Stripe, PayPal, etc.)
- Synchronisation de donnees entre differents logiciels
- Automatisation des workflows entre vos outils
- Authentication securisee (JWT, OAuth)
- Documentation API complete et claire
- Optimisation des performances et mise en cache
- Monitoring et alertes en cas de probleme

Les systemes deconnectes creent des silos de donnees, des saisies manuelles repetitives et des processus inefficaces. Vos outils ont besoin de communiquer pour que votre entreprise fonctionne de maniere fluide.

Que vous ayez besoin de connecter votre site e-commerce a votre systeme de comptabilite, integrer un systeme de paiement mobile, ou creer un pont entre votre application mobile et votre base de donnees, je peux construire la solution qui fait le lien.

Je suiv les meilleures pratiques de conception d'API, en m'assurant que vos endpoints sont intuitifs, bien documentes et securises. Chaque integration est testee rigoureusement pour garantir sa fiabilite en production.
                """,
                "icon": "fas fa-plug",
                "hero_description": "Je cree des integrations robustes qui connectent vos applications et permettent un flux de donnees harmonieux entre tous vos systemes.",
                "problem": "Les systemes deconnectes entrainent des silos de donnees, des saisies manuelles repetitives et des processus de travail inefficaces. Les entreprises ont besoin que leurs outils communiquent pour etre productives.",
                "audience": "Entreprises avec plusieurs systemes logiciels, societes SaaS, developpeurs d'applications mobiles, commerces en ligne ayant besoin de connecter leurs outils de paiement, et organisations cherchant a automatiser leurs processus metier.",
                "features": "Conception RESTful, authentification JWT et OAuth, documentation API complete, integrations tierces, gestion des erreurs, mise en cache, surveillance des performances.",
                "how_it_works": "J'analyse vos besoins en integration, je conçois l'architecture de l'API, je developpe les endpoints, je redige une documentation complete, et je teste rigoureusement chaque composant avant la mise en production.",
                "benefits": "Integrations fiables, endpoints bien documentes, authentification securisee, architecture evolutive, gain de temps considereable grace a l'automatisation.",
                "included": "Implementation complete de l'API, documentation technique, suite de tests, support d'integration, et assistance pendant la mise en production.",
                "is_featured": True,
                "is_active": True,
                "display_order": 3,
            },
            {
                "title": "Maintenance & Support Technique",
                "slug": "maintenance-support-technique",
                "short_description": "Maintien, amelioration et support continu de vos applications web pour garantir leur performance et securite dans le temps.",
                "description": """
Un projet web ne s'arrete pas au lancement. Pour rester performant, securise et pertinent, votre application a besoin d'un suivi regulier et d'ameliorations continues. Je vous offre un service de maintenance et support technique complet pour que votre plateforme fonctionne toujours a 100%.

Mes services de maintenance incluent :
- Surveillance et maintenance preventive de vos applications
- Mises a jour de securite et correction de vulnerabilites
- Optimisation des performances et de la vitesse de chargement
- Sauvegardes automatiques et plan de reprise d'activite
- Correction de bugs et resolution de problemes techniques
- Ajout de nouvelles fonctionnalites selon vos besoins
- Monitoring 24/7 avec alertes en temps reel
- Support technique reactif par email, telephone ou WhatsApp

Beaucoup d'entreprises negligent la maintenance de leur site web ou de leur application. Les resultats ? Des sites lents, des failles de securite, des temps d'arret non prevus, et des clients mecontents.

Avec un service de maintenance, vous avez l'esprit tranquille. Je m'occupe de tout : les mises a jour de securite, l'optimisation des performances, la surveillance des erreurs, et l'ajout de nouvelles fonctionnalites quand vous en avez besoin.

Je propose des forfaits mensuels adaptes a la taille de votre projet, avec des delais d'intervention garantis. En cas d'urgence, je suis disponible pour resoudre les problemes critiques rapidement.

Votre application est votre outil de travail le plus important. Elle merite d'etre entretenue par un professionnel qui la connait.
                """,
                "icon": "fas fa-tools",
                "hero_description": "Je maintiens et ameliore vos applications web pour qu'elles restent performantes, securisees et a jour en permanence.",
                "problem": "Negliger la maintenance d'une application web entraine des sites lents, des failles de securite, des temps d'arret imprevus, une perte de clients et des problemes techniques qui s'accumulent avec le temps.",
                "audience": "Entreprises ayant deja une application web ou un site en ligne, startups dont le produit numerique est en production, organisations qui veulent externaliser la maintenance technique, et e-commercants qui ont besoin d'une plateforme toujours disponible.",
                "features": "Maintenance preventive, mises a jour de securite, optimisation des performances, sauvegardes, correction de bugs, nouvelles fonctionnalites, monitoring, support technique reactif.",
                "how_it_works": "Nous definissons ensemble vos besoins de maintenance, je configure le monitoring de votre application, je m'occupe des mises a jour et optimisations regulieres, et je suis disponible en cas de probleme ou de demande d'evolution.",
                "benefits": "Tranquillite d'esprit, application toujours a jour et securisee, performances optimales, delais d'intervention garantis, evolutions progressives adaptees a vos besoins.",
                "included": "Surveillance continue, rapports mensuels d'activite, mises a jour de securite, backup automatique, support technique par email et telephone.",
                "is_featured": False,
                "is_active": True,
                "display_order": 4,
            },
        ]

        services = []
        for data in services_data:
            services.append(Service.objects.create(**data))
        return services

    def create_service_features(self, services):
        features = {
            services[0]: [
                "Applications web sur mesure avec Django et Python",
                "Design responsive fonctionnel sur tous les appareils",
                "Authentification et autorisation securisees",
                "Fonctionnalites en temps reel et notifications",
                "Conception et optimisation de base de donnees",
                "Deploiement, hebergement et mise en production",
                "Interface administrateur intuitive et complete",
                "Integration de systemes de paiement (Mobile Money, Carte)",
            ],
            services[1]: [
                "Audit technique complet de votre situation actuelle",
                "Etude de faisabilite et analyse des risques",
                "Recommandations personnalisees et actionnables",
                "Plan de developpement progressif et realiste",
                "Choix des technologies adaptees a votre budget",
                "Formation et accompagnement de vos equipes",
            ],
            services[2]: [
                "Conception et developpement d'API RESTful",
                "Integration avec les services de paiement (Mobile Money, Stripe)",
                "Synchronisation de donnees entre differents systemes",
                "Documentation API complete et interactive",
                "Authentification securisee JWT et OAuth",
                "Monitoring et surveillance des performances",
            ],
            services[3]: [
                "Maintenance preventive et surveillance continue",
                "Mises a jour de securite regulieres",
                "Optimisation des performances et de la vitesse",
                "Sauvegardes automatiques et plan de reprise",
                "Correction de bugs et resolution rapide",
                "Ajout de nouvelles fonctionnalites sur demande",
            ],
        }

        for service, feature_list in features.items():
            for i, feature_text in enumerate(feature_list):
                ServiceFeature.objects.create(
                    service=service,
                    feature=feature_text,
                    display_order=i + 1,
                )

    def create_experiences(self):
        experiences = [
            {
                "title": "Developpeur Full-Stack",
                "organization": "Indépendant",
                "location": "Bafoussam, Cameroun",
                "start_date": timezone.datetime(2021, 1, 1),
                "end_date": None,
                "is_current": True,
                "type": "freelance",
                "role": "Fondateur & Developpeur Principal",
                "description": "Conception et developpement de solutions digitales sur mesure pour des clients au Cameroun et a l'international, specialise dans les applications web, les API et la transformation digitale des entreprises.",
                "responsibilities": "Relation client, gestion de projet, recueil des besoins, architecture technique, developpement full-stack, deploiement et maintenance.",
                "tasks": "Developpement d'applications web avec Django et Python, creation d'API RESTful, integration de systemes de paiement, optimisation des bases de donnees, et accompagnement technique des clients.",
                "achievements": "Plus de 25 projets livres avec succes, 100% de taux de satisfaction client, creation de plateformes e-commerce et applications SaaS rentables.",
                "results": "Aide des dizaines d'entreprises a digitaliser leurs operations et a augmenter leur chiffre d'affaires grace a des solutions digitales performantes.",
                "display_order": 1,
                "is_published": True,
            },
            {
                "title": "Developpeur Web Full-Stack",
                "organization": "Projets Freelance & Collaborations",
                "location": "Cameroun & International",
                "start_date": timezone.datetime(2019, 6, 1),
                "end_date": timezone.datetime(2020, 12, 31),
                "is_current": False,
                "type": "freelance",
                "role": "Developpeur Full-Stack",
                "description": "Realisation de projets web diversifies pour des clients locaux et internationaux, allant des sites vitrines aux plateformes e-commerce complexes.",
                "responsibilities": "Gestion complete du cycle de developpement, de la conception a la mise en production, en passant par le test et l'optimisation.",
                "tasks": "Developpement de sites web et d'applications, creation d'interfaces utilisateur modernes, integration d'API tierces, et mise en place d'infrastructures techniques.",
                "achievements": "Construction d'un portfolio solide de projets, developpement d'expertise dans les technologies modernes, et etablissement de relations durables avec les clients.",
                "results": "Reputation professionnelle croissante et recommandations clients qui generent de nouvelles opportunites de travail.",
                "display_order": 2,
                "is_published": True,
            },
            {
                "title": "Licence en Informatique",
                "organization": "Universite de Bafoussam",
                "location": "Bafoussam, Cameroun",
                "start_date": timezone.datetime(2016, 10, 1),
                "end_date": timezone.datetime(2019, 7, 31),
                "is_current": False,
                "type": "academic",
                "role": "Etudiant",
                "description": "Formation complete en informatique couvrant les fondamentaux du developpement logiciel, les algorithmes, les structures de donnees et les technologies web modernes.",
                "responsibilities": "Travaux pratiques en laboratoire, projets de developpement, etudes de cas, et travail en equipe sur des projets informatiques.",
                "tasks": "Etude des algorithmes et structures de donnees, programmation en Python et Java, bases de donnees, developpement web, et methodes de genie logiciel.",
                "achievements": "Obtention du diplome avec mention, realisation de plusieurs projets academiques reussis, et participation active a des hackathons et competitions de programmation.",
                "results": "Acquisition de competences solides en developpement logiciel et en resolution de problemes techniques, base de ma carriere dans le developpement web.",
                "display_order": 3,
                "is_published": True,
            },
        ]
        for experience in experiences:
            Experience.objects.create(**experience)

    def create_technologies(self):
        technologies = [
            {"name": "Python", "icon": "fab fa-python", "display_order": 1},
            {"name": "Django", "icon": "fas fa-fire", "display_order": 2},
            {"name": "PostgreSQL", "icon": "fas fa-database", "display_order": 3},
            {"name": "JavaScript", "icon": "fab fa-js-square", "display_order": 4},
            {"name": "Tailwind CSS", "icon": "fas fa-wind", "display_order": 5},
            {"name": "HTML5", "icon": "fab fa-html5", "display_order": 6},
            {"name": "CSS3", "icon": "fab fa-css3-alt", "display_order": 7},
            {"name": "Docker", "icon": "fab fa-docker", "display_order": 8},
            {"name": "Git", "icon": "fab fa-git-alt", "display_order": 9},
            {"name": "Linux", "icon": "fab fa-linux", "display_order": 10},
        ]
        return [Technology.objects.create(**tech) for tech in technologies]

    def create_projects(self, technologies):
        projects_data = [
            {
                "title": "AutoLink - Plateforme Automobile",
                "slug": "autolink-plateforme-automobile",
                "short_description": "Plateforme web complete de vente et d'achat de vehicules d'occasion au Cameroun, avec gestion des annonces, recherche avancee et mise en relation acheteurs-vendeurs.",
                "context": "Le marche automobile camerounais manquait d'une plateforme moderne et fiable pour la vente de vehicules d'occasion. Les vendeurs publiaient sur les reseaux sociaux sans structure, et les acheteurs perdaient des heures a chercher sans trouver ce qu'ils voulaient. Il fallait une solution centralisee et professionnelle.",
                "problem": "Les particuliers et professionnels de l'automobile avaient besoin d'un outil simple pour publier leurs annonces avec des photos de qualite, permettre aux acheteurs de filtrer et rechercher facilement, et faciliter la mise en relation entre les deux parties. Les solutions existantes etrangeres ne correspondaient pas aux realites du marche local.",
                "approach": "J'ai commence par etudier le marche automobile camerounais, interviewe des vendeurs et des acheteurs pour comprendre leurs besoins reels. J'ai identifie les points de friction dans le processus actuel et concu une solution adaptee au contexte local, avec prise en compte des aspects comme les prix en francs CFA et les modeles de vehicules populaires au Cameroun.",
                "solution": "J'ai developpe une plateforme web complete avec Django et Python, integrant un systeme de gestion d'annonces avance avec photos multiples, des filtres de recherche detailles (marque, modele, annee, prix, localisation), un systeme de messagerie entre utilisateurs, et un tableau de bord administrateur pour gerer l'ensemble du contenu.",
                "features": "Publication d'annonces avec galerie photos, recherche avancee avec filtres multiples, systeme de messagerie integre, favoris et alertes, profil utilisateur, tableau de bord administrateur, systeme de signalement, et interface responsive mobile-first.",
                "result": "La plateforme a permis de centraliser le marche automobile local, facilitant des centaines de transactions. Les vendeurs gagnent du temps et les acheteurs trouvent rapidement le vehicule qui leur convient. Le trafic de la plateforme croit regulierement grace au bouche-a-oreille.",
                "role": "Conception, developpement et deploiement complet de la plateforme. Architecture technique, developpement backend et frontend, integration des fonctionnalites de recherche, et mise en production.",
                "client_name": "AutoLink Cameroun",
                "project_date": timezone.datetime(2024, 3, 1),
                "status": "completed",
                "live_url": "https://autolink.cohub.site",
                "github_url": "",
                "technologies": technologies[:5],
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Copal Satcheme - Portfolio Professionnel",
                "slug": "copal-satcheme-portfolio",
                "short_description": "Site portfolio personnel et vitrine professionnelle, concu pour presenter mes services, projets et competences de maniere attractive et convaincante.",
                "context": "En tant que developpeur freelance, il est essentiel d'avoir une vitrine professionnelle qui met en valeur son travail et ses competences. Le portfolio est souvent le premier contact avec un client potentiel, il devait donc etre impressionnant, rapide et facilement maintenable.",
                "problem": "Il me fallait un site qui me represente bien, qui mette en avant mes realisations passées de maniere convaincante, qui soit rapide a charger, optimise pour le referencement (SEO), et que je puisse mettre a jour facilement quand j'ajoute de nouveaux projets ou services.",
                "approach": "J'ai voulu construire quelque chose de different des templates generiques. J'ai concu chaque page en pensant a l'experience visiteur : navigation intuitive, presentation claire des projets, appel a l'action pertinent. J'ai aussi integre un systeme d'administration pour gerer le contenu sans toucher au code.",
                "solution": "J'ai developpe un site portfolio complet avec Django, integrant un systeme de gestion de contenu dynamique, une page de presentation des projets avec contexts et resultats detailles, un systeme de temoignages clients, et un formulaire de contact fonctionnel. Le tout est optimise pour le SEO et responsive sur tous les appareils.",
                "features": "Design moderne et professionnel, presentation detaillee des projets avec contexte et resultats, systeme de temoignages, formulaire de contact, optimisation SEO, administration dynamique, performance optimisee, et interface responsive.",
                "result": "Le portfolio est devenu mon meilleur outil de prospection. Les clients potentiels decouvre mon travail en ligne et me contactent directement. Le site genere des leads qualifies et m'a aide a decrocher plusieurs projets importants.",
                "role": "Conception UI/UX, developpement full-stack, integration du systeme de gestion de contenu, optimisation SEO, et deploiement. Ce projet est aussi une demonstration de mes competences techniques.",
                "client_name": "Copal Satcheme (Projet Personnel)",
                "project_date": timezone.datetime(2025, 1, 15),
                "status": "completed",
                "live_url": "https://copal-satcheme.cohub.site",
                "github_url": "https://github.com/stevecopal",
                "technologies": technologies[:6],
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "EauPourTous - Plateforme de Gestion de l'Eau",
                "slug": "eaupourtous-gestion-eau",
                "short_description": "Application web de gestion et de distribution de l'eau potable pour les communautes, avec suivi des livraisons, gestion des abonnements et tableau de bord analytique.",
                "context": "L'acces a l'eau potable reste un defi majeur dans de nombreuses communautes camerounaises. Une organisation engagee dans ce domaine cherchait a moderniser sa gestion des livraisons et a ameliorer le service rendu aux populations. Le systeme existant etait base sur des registres papier, source d'erreurs et de lenteurs.",
                "problem": "Il fallait creer un outil capable de gerer les abonnements clients, planifier et suivre les livraisons d'eau, suivre les paiements, et fournir des statistiques fiables aux gestionnaires. Le systeme devait etre simple a utiliser, meme pour des utilisateurs non-techniques, et accessible depuis des appareils mobiles dans les zones a connectivite limitee.",
                "approach": "J'ai analyse en profondeur le processus de gestion actuel, identifie les goulets d'etranglement, et concu une solution qui simplifie chaque etape. J'ai donne une attention particuliere a l'interface utilisateur pour qu'elle soit intuitive, et j'ai optimise l'application pour fonctionner meme avec une connexion internet lente.",
                "solution": "J'ai developpe une application web complete avec Django, comprenant un systeme de gestion des abonnements, un module de planification et suivi des livraisons, un tableau de bord analytique avec graphiques, et un systeme de notifications pour informer les clients. L'application est responsive et fonctionne bien sur mobile.",
                "features": "Gestion des abonnements clients, planification des livraisons, suivi en temps reel, systeme de paiement et suivi des factures, tableau de bord avec statistiques et graphiques, notifications automatiques, gestion des zones de livraison, et rapport d'activite mensuel.",
                "result": "Le systeme a reduit les erreurs de gestion de 80%, ameliore la ponctualite des livraisons, et donne aux gestionnaires une visibilite complete sur leur activite. Les clients sont mieux informes et plus satisfaits du service.",
                "role": "Conception et developpement complet de l'application. Analyse des besoins, architecture technique, developpement backend et frontend, integration du tableau de bord analytique, et formation des utilisateurs.",
                "client_name": "EauPourTous SARL",
                "project_date": timezone.datetime(2025, 6, 1),
                "status": "completed",
                "live_url": "https://eaupourtoussarl.com",
                "github_url": "",
                "technologies": technologies[:5],
                "is_featured": True,
                "is_published": True,
            },
        ]

        created_projects = []
        for data in projects_data:
            techs = data.pop("technologies")
            p = Project.objects.create(**data)
            p.technologies.set(techs)
            created_projects.append(p)

        return created_projects

    def create_project_images(self, projects):
        captions = [
            "Page d'accueil de la plateforme AutoLink",
            "Presentation des services du portfolio",
            "Tableau de bord de gestion EauPourTous",
        ]
        for i, project in enumerate(projects):
            ProjectImage.objects.create(
                project=project,
                caption=captions[i % len(captions)],
                display_order=0,
            )

    def create_testimonials(self):
        testimonials = [
            {
                "name": "Mbarga Jean-Pierre",
                "position": "Directeur",
                "company": "AutoLink Cameroun",
                "testimonial": "Copal a transforme notre vision en une plateforme professionnelle qui depasse nos attentes. Sa capacite a comprendre nos besoins et a proposer des solutions pertinentes est impressionnante. Le projet a ete livre dans les delais et le resultat est exactement ce que nous voulions. Je le recommande vivement a quiconque cherche un developpeur serieux et competent.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 1,
            },
            {
                "name": "Nkoumou Alice",
                "position": "Gestionnaire",
                "company": "EauPourTous SARL",
                "testimonial": "Grace a l'application developpee par Copal, nous avons gagne un temps considerable dans la gestion de nos livraisons. L'outil est simple, rapide et tres fonctionnel. Il a su comprendre les realites de notre terrain et creer une solution qui s'adapte parfaitement a nos besoins. Son professionnalisme et sa reactivite sont remarquables.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 2,
            },
            {
                "name": "Fotso Samuel",
                "position": "Entrepreneur",
                "company": "TechStartup Cameroun",
                "testimonial": "J'ai fait appel a Copal pour la creation de mon application web et je ne pouvais pas etre plus satisfait. Il a su traduire mes idees en une solution technique solide et elegante. Sa capacite a expliquer les choses simplement et a impliquer le client tout au long du projet est un vrai atout. C'est un developpeur d'excellence.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 3,
            },
            {
                "name": "Bikoko Christine",
                "position": "Responsable Communication",
                "company": "Groupe Scolaire Les Palmiers",
                "testimonial": "Le site web que Copal a cree pour notre etablissement est moderne, rapide et facile a mettre a jour. Il a pris le temps de comprendre notre identite et nos besoins specifiques. Le resultat est une vitrine en ligne dont nous sommes fiers et qui nous a permis d'attirer de nouveaux eleves. Merci pour ce travail remarquable.",
                "rating": 5,
                "is_featured": False,
                "is_active": True,
                "display_order": 4,
            },
        ]
        for testimonial in testimonials:
            Testimonial.objects.create(**testimonial)

    def create_seo(self):
        seo_data = [
            {
                "page": "home",
                "seo_title": "Copal Satcheme | Developpeur Full-Stack & Solutions Digitales au Cameroun",
                "seo_description": "Portfolio professionnel de Copal Satcheme, developpeur full-base a Bafoussam, Cameroun. Je developpe des applications web modernes, des API et des solutions digitales avec Django, Python et des technologies de pointe.",
            },
            {
                "page": "about",
                "seo_title": "A Propos | Copal Satcheme - Developpeur Full-Stack Cameroun",
                "seo_description": "Decouvrez Copal Satcheme, developpeur full-stack base a Bafoussam au Cameroun. Son parcours, ses competences et son experience dans la creation de solutions digitales pour les entreprises.",
            },
            {
                "page": "services",
                "seo_title": "Services | Copal Satcheme - Developpement Web, Conseil & Integration au Cameroun",
                "seo_description": "Services professionnels de developpement d'applications web, conseil et strategie digitale, integration d'API et maintenance technique. Des solutions adaptees a vos besoins metier au Cameroun.",
            },
            {
                "page": "experience",
                "seo_title": "Parcours | Copal Satcheme - Experience en Developpement Web",
                "seo_description": "Le parcours professionnel de Copal Satcheme, developpeur full-base a Bafoussam. Plus de 5 ans d'experience dans la creation de solutions digitales performantes.",
            },
            {
                "page": "projects",
                "seo_title": "Projets | Copal Satcheme - Realisations en Developpement Web au Cameroun",
                "seo_description": "Decouvrez les projets realises par Copal Satcheme : plateformes e-commerce, applications de gestion, sites web professionnels. Chaque projet est une solution qui resout un vrai probleme.",
            },
            {
                "page": "contact",
                "seo_title": "Contact | Copal Satcheme - Parlons de Votre Projet",
                "seo_description": "Contactez Copal Satcheme pour votre projet de developpement web, creation d'application ou conseil technique. Disponible a Bafoussam et pour des projets a distance partout au Cameroun.",
            },
        ]
        for seo in seo_data:
            SEO.objects.create(**seo)

    def create_tools(self):
        tools_data = [
            {"name": "Python", "icon": "fab fa-python", "category": "language", "display_order": 1},
            {"name": "Django", "icon": "fas fa-fire", "category": "framework", "display_order": 2},
            {"name": "Docker", "icon": "fab fa-docker", "category": "tool", "display_order": 3},
        ]
        for tool in tools_data:
            Tool.objects.create(**tool)
