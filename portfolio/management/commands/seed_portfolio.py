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
            full_name="Steve Satcheme",
            professional_name="Steve Satcheme",
            professional_title="Full-Stack Developer & Digital Solutions Builder",
            short_bio="I design and build modern, scalable, and user-focused digital solutions that help businesses grow.",
            biography="""
I'm a passionate Full-Stack Developer with over 3 years of experience building modern web applications. I specialize in Django, Python, PostgreSQL, and frontend technologies like Tailwind CSS and JavaScript.

My approach is simple: I listen to your needs, understand your problem, and build a solution that works. I believe technology should serve people, not the other way around.

Every project I take on gets my full attention. I write clean, maintainable code and deliver solutions that are built to last. Whether you need a complete web application, a custom API, or technical consulting, I'm here to help.

When I'm not coding, I'm exploring new technologies, contributing to open source projects, or sharing what I've learned through technical articles.
            """,
            location="Douala",
            country="Cameroon",
            city="Douala",
            email="steve@copal.cm",
            phone="+237 699 123 456",
            whatsapp="+237 699 123 456",
            availability_status=True,
            availability_message="Available for new projects",
        )

    def create_social_links(self):
        social_links = [
            {
                "name": "GitHub",
                "platform": "github",
                "url": "https://github.com/stevesatcheme",
                "icon": "fab fa-github",
                "display_order": 1,
            },
            {
                "name": "LinkedIn",
                "platform": "linkedin",
                "url": "https://linkedin.com/in/stevesatcheme",
                "icon": "fab fa-linkedin",
                "display_order": 2,
            },
            {
                "name": "Twitter",
                "platform": "x",
                "url": "https://x.com/stevesatcheme",
                "icon": "fab fa-x-twitter",
                "display_order": 3,
            },
            {
                "name": "WhatsApp",
                "platform": "whatsapp",
                "url": "https://wa.me/237699123456",
                "icon": "fab fa-whatsapp",
                "display_order": 4,
            },
        ]
        for link in social_links:
            SocialLink.objects.create(**link)

    def create_site_settings(self):
        return SiteSettings.objects.create(
            site_name="Steve Satcheme | Portfolio",
            slogan="Building Digital Solutions That Work",
            short_description="Full-Stack Developer & Digital Solutions Builder",
            footer_text="Turning ideas into reality through code",
            copyright_text="© 2026 Steve Satcheme. All rights reserved.",
            primary_email="steve@copal.cm",
            year=2026,
            is_active=True,
            maintenance_mode=False,
        )

    def create_services(self):
        services_data = [
            {
                "title": "Web Application Development",
                "slug": "web-application-development",
                "short_description": "Custom web applications built with modern technologies, tailored to your business needs.",
                "description": """
I build responsive, modern web applications using Django and Python for the backend, combined with Tailwind CSS and JavaScript for beautiful, functional frontends.

My web development services include:
- Custom Django applications
- Responsive frontend development
- Database design and optimization
- User authentication and authorization systems
- Deployment and hosting setup

Every project starts with understanding your needs. I don't believe in one-size-fits-all solutions. Your application will be built specifically for your use case.
                """,
                "icon": "fas fa-globe",
                "hero_description": "I build custom web applications that are fast, secure, and scalable. From simple landing pages to complex enterprise solutions.",
                "problem": "Many businesses struggle with off-the-shelf software that doesn't quite fit their needs. They waste time and money trying to adapt their processes to rigid tools.",
                "audience": "Businesses that need custom web applications, startups looking to launch their MVP, and companies wanting to digitize their operations.",
                "features": "Custom development, responsive design, secure authentication, real-time features, API integration, and ongoing support.",
                "how_it_works": "We start with a discovery call to understand your needs. Then I design the solution, develop it in sprints, and deploy it once you're satisfied.",
                "benefits": "A solution built specifically for your needs, modern and maintainable code, scalable architecture, and dedicated support.",
                "included": "Full source code, documentation, deployment support, and 30 days of post-launch support.",
                "is_featured": True,
                "is_active": True,
                "display_order": 1,
            },
            {
                "title": "API Development & Integration",
                "slug": "api-development-integration",
                "short_description": "RESTful APIs that connect your systems and enable seamless data flow between applications.",
                "description": """
I design and develop RESTful APIs that enable seamless communication between your frontend and backend systems.

My API development services include:
- RESTful API design and development
- Authentication and authorization (JWT, OAuth)
- API documentation (OpenAPI/Swagger)
- Third-party API integrations
- Performance optimization

I follow best practices for API design, ensuring your endpoints are intuitive, well-documented, and secure.
                """,
                "icon": "fas fa-plug",
                "hero_description": "I create robust APIs that connect your applications and enable seamless data flow across your systems.",
                "problem": "Disconnected systems lead to data silos, manual data entry, and inefficient workflows. Businesses need their tools to communicate.",
                "audience": "SaaS companies, mobile app developers, businesses with multiple software systems, and companies needing system integrations.",
                "features": "RESTful design, authentication, rate limiting, documentation, error handling, and versioning.",
                "how_it_works": "I analyze your requirements, design the API architecture, develop the endpoints, write comprehensive documentation, and test thoroughly.",
                "benefits": "Reliable integrations, well-documented endpoints, secure authentication, and scalable architecture.",
                "included": "Full API implementation, documentation, testing suite, and integration support.",
                "is_featured": True,
                "is_active": True,
                "display_order": 2,
            },
            {
                "title": "Technical Consulting",
                "slug": "technical-consulting",
                "short_description": "Expert guidance on architecture, technology choices, and development best practices.",
                "description": """
Need help with your project architecture or technical decisions? I provide consulting services to help you make the right choices.

My consulting services include:
- Project architecture review
- Technology selection and stack recommendations
- Code review and quality assessment
- Performance auditing
- Development process optimization

I'll help you avoid common pitfalls and make informed decisions that save you time and money.
                """,
                "icon": "fas fa-lightbulb",
                "hero_description": "Get expert advice on your technical challenges. I help you make the right decisions for your project.",
                "problem": "Making the wrong technical decisions early can cost months of work and thousands of dollars. You need an experienced eye to guide you.",
                "audience": "Startups planning their tech stack, teams facing architectural challenges, and businesses evaluating their technical debt.",
                "features": "Architecture review, stack recommendations, code audit, performance analysis, and actionable recommendations.",
                "how_it_works": "I review your current setup, identify issues and opportunities, and provide a detailed report with clear recommendations.",
                "benefits": "Avoid costly mistakes, optimize your development process, and build a solid foundation for growth.",
                "included": "Detailed analysis report, recommendations document, and follow-up consultation.",
                "is_featured": False,
                "is_active": True,
                "display_order": 3,
            },
        ]

        services = []
        for data in services_data:
            services.append(Service.objects.create(**data))
        return services

    def create_service_features(self, services):
        features = {
            services[0]: [
                "Custom Django applications tailored to your needs",
                "Responsive design that works on all devices",
                "Secure user authentication and authorization",
                "Real-time features and notifications",
                "Database design and optimization",
                "Deployment and hosting setup",
            ],
            services[1]: [
                "RESTful API design following best practices",
                "JWT and OAuth authentication",
                "Comprehensive API documentation",
                "Third-party service integrations",
                "Rate limiting and security measures",
                "Performance optimization",
            ],
            services[2]: [
                "In-depth architecture review",
                "Technology stack recommendations",
                "Code quality assessment",
                "Performance auditing",
                "Development process optimization",
                "Actionable improvement roadmap",
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
                "title": "Full-Stack Developer",
                "organization": "TechFlow Solutions",
                "location": "Douala, Cameroon",
                "start_date": timezone.datetime(2022, 3, 1),
                "end_date": None,
                "is_current": True,
                "type": "professional",
                "role": "Lead Developer",
                "description": "Leading the development of web applications and APIs for clients across various industries.",
                "responsibilities": "Architecture design, code review, client communication, and full-stack development.",
                "tasks": "Building scalable web applications, optimizing database queries, implementing new features, and mentoring junior developers.",
                "achievements": "Delivered 15+ successful projects, improved application performance by 40%, and established development best practices.",
                "results": "Increased client satisfaction by 35% and reduced project delivery time by 25%.",
                "display_order": 1,
                "is_published": True,
            },
            {
                "title": "Freelance Developer",
                "organization": "Self-Employed",
                "location": "Remote",
                "start_date": timezone.datetime(2020, 6, 1),
                "end_date": timezone.datetime(2022, 2, 28),
                "is_current": False,
                "type": "freelance",
                "role": "Full-Stack Developer",
                "description": "Building custom web solutions for clients worldwide, from e-commerce platforms to SaaS applications.",
                "responsibilities": "Client relations, project management, requirements gathering, and full development lifecycle.",
                "tasks": "Developing web applications, creating APIs, integrating third-party services, and providing technical consulting.",
                "achievements": "Completed 20+ projects, maintained 100% client satisfaction rate, and built long-term client relationships.",
                "results": "Generated $50K+ in revenue and established a strong professional network.",
                "display_order": 2,
                "is_published": True,
            },
            {
                "title": "Bachelor's in Computer Science",
                "organization": "University of Douala",
                "location": "Douala, Cameroon",
                "start_date": timezone.datetime(2016, 9, 1),
                "end_date": timezone.datetime(2020, 6, 30),
                "is_current": False,
                "type": "academic",
                "role": "Student",
                "description": "Comprehensive education in computer science fundamentals, software engineering, and web technologies.",
                "responsibilities": "Academic research, project development, and collaborative learning.",
                "tasks": "Studying algorithms, data structures, databases, and software development methodologies.",
                "achievements": "Graduated with honors, led student programming club, and completed 10+ academic projects.",
                "results": "Built strong foundation in software development and problem-solving skills.",
                "display_order": 3,
                "is_published": True,
            },
        ]
        for experience in experiences:
            Experience.objects.create(**experience)

    def create_technologies(self):
        technologies = [
            {"name": "Python", "icon": "fab fa-python", "display_order": 1},
            {"name": "Django", "icon": "fas fa-code", "display_order": 2},
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
                "title": "E-Commerce Platform",
                "slug": "e-commerce-platform",
                "short_description": "A full-featured e-commerce solution with product management, cart, and payment processing.",
                "context": "A local retail business wanted to expand online but was struggling with existing platforms that were too expensive and inflexible.",
                "problem": "They needed a custom solution that could handle their unique product catalog, multiple payment methods, and integrate with their existing inventory system.",
                "approach": "I started by analyzing their current workflow, identifying pain points, and designing a solution that addressed their specific needs.",
                "solution": "Built a Django-based e-commerce platform with product management, shopping cart, checkout flow, and integration with mobile money and card payments.",
                "features": "Product catalog, search and filtering, shopping cart, multiple payment gateways, order tracking, admin dashboard.",
                "result": "The platform launched successfully and increased their online sales by 150% in the first 3 months.",
                "role": "Full development from concept to deployment, including database design, backend logic, frontend implementation, and payment integration.",
                "client_name": "ShopCameroon",
                "project_date": timezone.datetime(2023, 5, 15),
                "status": "completed",
                "live_url": "https://shopcameroon.example.com",
                "github_url": "https://github.com/stevesatcheme/shopcameroon",
                "technologies": technologies[:5],
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Task Management App",
                "slug": "task-management-app",
                "short_description": "A collaborative task management tool for remote teams with real-time updates.",
                "context": "A growing startup was struggling to manage tasks across their distributed team. Existing tools were either too complex or too expensive.",
                "problem": "They needed a simple, intuitive tool that could handle task assignment, tracking, and team collaboration without the bloat of enterprise solutions.",
                "approach": "I conducted user interviews to understand their workflow, then designed a minimal but powerful solution.",
                "solution": "Created a Django application with a clean interface, real-time updates using polling, file attachments, and team collaboration features.",
                "features": "Task creation and assignment, project boards, file attachments, comments, notifications, team management.",
                "result": "The app improved team productivity by 30% and is now used by 50+ teams daily.",
                "role": "End-to-end development including UX design, database architecture, backend logic, and frontend implementation.",
                "client_name": "TeamWork Inc.",
                "project_date": timezone.datetime(2023, 9, 20),
                "status": "completed",
                "live_url": "https://teamwork-app.example.com",
                "github_url": "https://github.com/stevesatcheme/taskmanager",
                "technologies": technologies[:4],
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Real Estate Listings",
                "slug": "real-estate-listings",
                "short_description": "A modern property listing platform with search, filters, and agent management.",
                "context": "A real estate agency needed to modernize their property listings and make them accessible to a wider audience.",
                "problem": "Their manual process of managing listings via spreadsheets and emails was inefficient and prone to errors.",
                "approach": "I analyzed their current process, identified bottlenecks, and designed an automated solution.",
                "solution": "Developed a property listing platform with advanced search, geolocation, image galleries, and agent management.",
                "features": "Property search, advanced filters, map view, image galleries, agent profiles, inquiry forms, analytics dashboard.",
                "result": "The platform reduced listing management time by 60% and increased qualified leads by 45%.",
                "role": "Full development including database design, search implementation, and admin dashboard.",
                "client_name": "HomeFind Cameroon",
                "project_date": timezone.datetime(2024, 1, 10),
                "status": "completed",
                "live_url": "https://homefind.example.com",
                "github_url": "https://github.com/stevesatcheme/realestate",
                "technologies": technologies[:6],
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Restaurant Management System",
                "slug": "restaurant-management-system",
                "short_description": "An all-in-one restaurant management solution with ordering, inventory, and reporting.",
                "context": "A restaurant chain wanted to digitize their operations and improve customer experience.",
                "problem": "They were losing money due to inefficient inventory management, slow order processing, and lack of customer data.",
                "approach": "I mapped out their entire workflow from order to delivery, identifying opportunities for automation and improvement.",
                "solution": "Built a comprehensive system covering online ordering, table reservations, inventory tracking, and business analytics.",
                "features": "Online ordering, table reservations, menu management, inventory tracking, staff scheduling, analytics dashboard.",
                "result": "The system reduced order processing time by 40% and increased customer retention by 25%.",
                "role": "Lead developer responsible for architecture design, database optimization, and full-stack implementation.",
                "client_name": "FoodChain Africa",
                "project_date": timezone.datetime(2024, 5, 1),
                "status": "completed",
                "live_url": "https://foodchain.example.com",
                "github_url": "https://github.com/stevesatcheme/restaurant",
                "technologies": technologies[:7],
                "is_featured": False,
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
            "Homepage view",
            "Dashboard interface",
            "Mobile responsive view",
            "Admin panel",
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
                "name": "Marie Dupont",
                "position": "CEO",
                "company": "TechStart Paris",
                "testimonial": "Steve delivered an exceptional e-commerce platform that exceeded our expectations. His attention to detail and commitment to quality is outstanding. He's not just a developer, he's a problem solver.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 1,
            },
            {
                "name": "James Wilson",
                "position": "CTO",
                "company": "InnovateTech",
                "testimonial": "Working with Steve was a great experience. He understood our technical requirements perfectly and delivered a robust, scalable solution. His communication skills are excellent.",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 2,
            },
            {
                "name": "Amina Hassan",
                "position": "Founder",
                "company": "AfriTech Solutions",
                "testimonial": "Steve built our task management app and it transformed how our team works. The application is intuitive, fast, and reliable. He delivered on time and within budget. Highly recommended!",
                "rating": 5,
                "is_featured": True,
                "is_active": True,
                "display_order": 3,
            },
            {
                "name": "Pierre Njoya",
                "position": "Director",
                "company": "CamReal Estate",
                "testimonial": "Our real estate platform is now our most valuable asset. Steve understood our vision and brought it to life. The search functionality and user experience are fantastic.",
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
                "seo_title": "Steve Satcheme | Full-Stack Developer & Digital Solutions Builder",
                "seo_description": "Professional portfolio of Steve Satcheme. I build modern web applications, APIs, and digital solutions using Django, Python, and cutting-edge technologies.",
            },
            {
                "page": "about",
                "seo_title": "About Steve Satcheme | Full-Stack Developer",
                "seo_description": "Learn more about Steve Satcheme - his background, skills, and experience building digital solutions for businesses worldwide.",
            },
            {
                "page": "services",
                "seo_title": "Services | Steve Satcheme - Web Development & Consulting",
                "seo_description": "Professional web development services including custom applications, API development, and technical consulting. Let's build something great together.",
            },
            {
                "page": "experience",
                "seo_title": "Experience | Steve Satcheme - Professional Background",
                "seo_description": "Discover my professional journey, from freelance projects to leading development teams. 3+ years of building digital solutions.",
            },
            {
                "page": "projects",
                "seo_title": "Projects | Steve Satcheme - Portfolio of Work",
                "seo_description": "Explore my portfolio of web applications, APIs, and digital solutions. Each project tells a story of solving real problems.",
            },
            {
                "page": "contact",
                "seo_title": "Contact | Steve Satcheme - Let's Work Together",
                "seo_description": "Ready to start your project? Get in touch with Steve Satcheme for web development, API creation, and technical consulting.",
            },
        ]
        for seo in seo_data:
            SEO.objects.create(**seo)

    def create_tools(self):
        tools_data = [
            {"name": "Python", "icon": "fab fa-python", "category": "language", "display_order": 1},
            {"name": "Django", "icon": "fas fa-fire", "category": "framework", "display_order": 2},
            {"name": "JavaScript", "icon": "fab fa-js-square", "category": "language", "display_order": 3},
            {"name": "PostgreSQL", "icon": "fas fa-database", "category": "database", "display_order": 4},
            {"name": "Docker", "icon": "fab fa-docker", "category": "tool", "display_order": 5},
            {"name": "Git", "icon": "fab fa-git-alt", "category": "tool", "display_order": 6},
            {"name": "Linux", "icon": "fab fa-linux", "category": "tool", "display_order": 7},
            {"name": "Tailwind CSS", "icon": "fas fa-wind", "category": "framework", "display_order": 8},
            {"name": "VS Code", "icon": "fas fa-code", "category": "tool", "display_order": 9},
            {"name": "REST APIs", "icon": "fas fa-plug", "category": "framework", "display_order": 10},
        ]
        for tool in tools_data:
            Tool.objects.create(**tool)
