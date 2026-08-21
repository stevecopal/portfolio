from django.core.management.base import BaseCommand
from django.utils import timezone
from portfolio.models import (
    Profile,
    SocialLink,
    Statistic,
    Service,
    ServiceFeature,
    SkillCategory,
    Skill,
    Experience,
    Project,
    ProjectImage,
    Technology,
    Article,
    Category,
    Tag,
    Testimonial,
    SiteSettings,
    SEO,
)

class Command(BaseCommand):
    help = 'Seeds the portfolio with initial data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding portfolio data...'))
        
        # Clear existing data
        self.clear_existing_data()
        
        # Create Profile
        profile = self.create_profile()
        
        
        # Create Social Links
        self.create_social_links()
        
        # Create Site Settings
        site_settings = self.create_site_settings()
        
        # Create Statistics
        self.create_statistics()
        
        # Create Services
        services = self.create_services()
        
        # Create Service Features
        self.create_service_features(services)
        
        # Create Skill Categories and Skills
        self.create_skills()
        
        # Create Experiences
        self.create_experiences()
        
        # Create Technologies
        technologies = self.create_technologies()
        
        # Create Projects
        projects = self.create_projects(technologies)
        
        # Create Project Images
        self.create_project_images(projects)
        
        # Create Categories and Tags
        categories, tags = self.create_categories_and_tags()
        
        # Create Articles
        self.create_articles(profile, categories, tags)
        
        # Create Testimonials
        self.create_testimonials()
        
        # Create SEO
        self.create_seo()
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded portfolio data!'))

    def clear_existing_data(self):
        models = [
            Profile, SocialLink, Statistic, Service, ServiceFeature,
            SkillCategory, Skill, Experience, Project, ProjectImage, Technology,
            Article, Category, Tag, Testimonial, SiteSettings, SEO
        ]
        for model in models:
            model.objects.all().delete()

    def create_profile(self):
        return Profile.objects.create(
            full_name="Steve Satcheme",
            professional_name="Steve Satcheme",
            professional_title="Full-Stack Developer & Digital Solutions Builder",
            short_bio="I design and develop modern, scalable, and user-focused digital solutions.",
            biography="""
            Passionate Full-Stack Developer with over 3 years of experience in building modern web applications.
            Specialized in Django, Python, PostgreSQL, and modern frontend technologies like Tailwind CSS and JavaScript.
            
            I believe in creating clean, maintainable code and building solutions that solve real problems.
            My approach combines technical expertise with a strong focus on user experience and design.
            
            When I'm not coding, you can find me writing about technology, contributing to open source,
            or exploring new frameworks and tools to expand my skillset.
            """,
            location="Douala",
            country="Cameroon",
            city="Douala",
            email="steve@copal.cm",
            phone="+237 123 456 789",
            whatsapp="+237 123 456 789",
            availability_status=True,
            availability_message="Available for new projects",
        )


    def create_social_links(self):
        social_links = [
            {"name": "GitHub", "platform": "github", "url": "https://github.com/stevesatcheme", "icon": "fab fa-github", "display_order": 1},
            {"name": "LinkedIn", "platform": "linkedin", "url": "https://linkedin.com/in/stevesatcheme", "icon": "fab fa-linkedin", "display_order": 2},
            {"name": "Twitter", "platform": "x", "url": "https://twitter.com/stevesatcheme", "icon": "fab fa-twitter", "display_order": 3},
            {"name": "WhatsApp", "platform": "whatsapp", "url": "https://wa.me/237123456789", "icon": "fab fa-whatsapp", "display_order": 4},
        ]
        for link in social_links:
            SocialLink.objects.create(**link)

    def create_site_settings(self):
        return SiteSettings.objects.create(
            site_name="Steve Satcheme | Portfolio",
            slogan="Building Digital Solutions",
            short_description="Full-Stack Developer & Digital Solutions Builder",
            footer_text="Building modern, scalable digital solutions",
            copyright_text="© 2026 Steve Satcheme. All rights reserved.",
            primary_email="steve@copal.cm",
            year=2026,
            is_active=True,
            maintenance_mode=False,
        )

    def create_statistics(self):
        statistics = [
            {"label": "Years Experience", "value": 3, "icon": "fas fa-clock", "display_order": 1},
            {"label": "Projects Completed", "value": 20, "icon": "fas fa-project-diagram", "display_order": 2},
            {"label": "Technologies", "value": 10, "icon": "fas fa-code", "display_order": 3},
            {"label": "Happy Clients", "value": 10, "icon": "fas fa-users", "display_order": 4},
        ]
        for stat in statistics:
            Statistic.objects.create(**stat)

    def create_services(self):
        services = [
            {
                "title": "Web Development",
                "short_description": "Custom web applications tailored to your business needs.",
                "description": "I build responsive, modern web applications using Django and Python for the backend, combined with Tailwind CSS and JavaScript for beautiful, functional frontends.",
                "icon": "fas fa-globe",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "title": "Backend Development",
                "short_description": "Robust backend systems and APIs.",
                "description": "Specialized in building scalable backend systems using Django, Django REST Framework, and PostgreSQL. I create efficient APIs and database architectures that power your applications.",
                "icon": "fas fa-server",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "title": "API Development",
                "short_description": "RESTful APIs for your applications.",
                "description": "I design and develop RESTful APIs that enable seamless communication between your frontend and backend systems.",
                "icon": "fas fa-plug",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "title": "Technical Consulting",
                "short_description": "Expert advice for your technical challenges.",
                "description": "Need help with your project architecture or technical decisions? I provide consulting services to help you make the right choices.",
                "icon": "fas fa-lightbulb",
                "is_featured": False,
                "display_order": 4,
            },
        ]
        return [Service.objects.create(**service) for service in services]

    def create_service_features(self, services):
        features = {
            services[0]: [
                "Custom Django applications",
                "Responsive frontend development",
                "Database design and optimization",
                "User authentication systems",
            ],
            services[1]: [
                "Python backend development",
                "Database architecture",
                "API integration",
                "Performance optimization",
            ],
            services[2]: [
                "RESTful API design",
                "JWT authentication",
                "API documentation",
                "Third-party integrations",
            ],
            services[3]: [
                "Project architecture review",
                "Technology selection",
                "Code review",
                "Performance auditing",
            ],
        }
        
        for service, feature_list in features.items():
            for i, feature_text in enumerate(feature_list):
                ServiceFeature.objects.create(
                    service=service,
                    feature=feature_text,
                    display_order=i + 1,
                )

    def create_skills(self):
        # Create categories
        backend = SkillCategory.objects.create(name="Backend", display_order=1)
        frontend = SkillCategory.objects.create(name="Frontend", display_order=2)
        database = SkillCategory.objects.create(name="Database", display_order=3)
        devops = SkillCategory.objects.create(name="DevOps", display_order=4)
        tools = SkillCategory.objects.create(name="Tools", display_order=5)
        
        # Create skills
        skills = [
            # Backend
            {"name": "Python", "category": backend, "level": "expert", "years_experience": 3, "display_order": 1, "is_featured": True},
            {"name": "Django", "category": backend, "level": "expert", "years_experience": 3, "display_order": 2, "is_featured": True},
            {"name": "Django REST Framework", "category": backend, "level": "advanced", "years_experience": 2, "display_order": 3, "is_featured": True},
            {"name": "REST APIs", "category": backend, "level": "advanced", "years_experience": 2, "display_order": 4, "is_featured": True},
            {"name": "JWT Authentication", "category": backend, "level": "intermediate", "years_experience": 2, "display_order": 5, "is_featured": False},
            
            # Frontend
            {"name": "HTML5", "category": frontend, "level": "expert", "years_experience": 3, "display_order": 1, "is_featured": True},
            {"name": "CSS3", "category": frontend, "level": "expert", "years_experience": 3, "display_order": 2, "is_featured": True},
            {"name": "JavaScript", "category": frontend, "level": "advanced", "years_experience": 3, "display_order": 3, "is_featured": True},
            {"name": "Tailwind CSS", "category": frontend, "level": "expert", "years_experience": 2, "display_order": 4, "is_featured": True},
            
            # Database
            {"name": "PostgreSQL", "category": database, "level": "intermediate", "years_experience": 2, "display_order": 1, "is_featured": True},
            {"name": "SQLite", "category": database, "level": "intermediate", "years_experience": 2, "display_order": 2, "is_featured": False},
            
            # DevOps
            {"name": "Docker", "category": devops, "level": "intermediate", "years_experience": 1, "display_order": 1, "is_featured": True},
            {"name": "Git", "category": devops, "level": "advanced", "years_experience": 3, "display_order": 2, "is_featured": True},
            {"name": "GitHub", "category": devops, "level": "advanced", "years_experience": 3, "display_order": 3, "is_featured": False},
            
            # Tools
            {"name": "VS Code", "category": tools, "level": "expert", "years_experience": 3, "display_order": 1, "is_featured": False},
            {"name": "Postman", "category": tools, "level": "intermediate", "years_experience": 2, "display_order": 2, "is_featured": False},
        ]
        
        for skill in skills:
            Skill.objects.create(**skill)

    def create_experiences(self):
        experiences = [
            {
                "title": "Full-Stack Developer",
                "company": "Tech Solutions Inc.",
                "location": "Douala, Cameroon",
                "description": "Developed and maintained web applications using Django and PostgreSQL. Implemented RESTful APIs and integrated third-party services. Collaborated with designers to create responsive, user-friendly interfaces.",
                "start_date": timezone.datetime(2021, 6, 1),
                "end_date": timezone.datetime(2023, 12, 31),
                "is_current": False,
                "type": "professional",
                "display_order": 1,
            },
            {
                "title": "Freelance Developer",
                "company": "Self-Employed",
                "location": "Remote",
                "description": "Worked on various projects for clients around the world. Built custom web applications, e-commerce platforms, and content management systems.",
                "start_date": timezone.datetime(2020, 1, 1),
                "end_date": timezone.datetime(2021, 5, 31),
                "is_current": False,
                "type": "freelance",
                "display_order": 2,
            },
            {
                "title": "Computer Science",
                "company": "University of Douala",
                "location": "Douala, Cameroon",
                "description": "Bachelor's degree in Computer Science. Gained strong foundation in programming, algorithms, and software engineering principles.",
                "start_date": timezone.datetime(2016, 9, 1),
                "end_date": timezone.datetime(2020, 6, 30),
                "is_current": False,
                "type": "academic",
                "display_order": 3,
            },
        ]
        for experience in experiences:
            Experience.objects.create(**experience)

    def create_technologies(self):
        technologies = [
            {"name": "Django", "display_order": 1},
            {"name": "Python", "display_order": 2},
            {"name": "PostgreSQL", "display_order": 3},
            {"name": "JavaScript", "display_order": 4},
            {"name": "Tailwind CSS", "display_order": 5},
            {"name": "HTML5", "display_order": 6},
            {"name": "CSS3", "display_order": 7},
            {"name": "Docker", "display_order": 8},
        ]
        return [Technology.objects.create(**tech) for tech in technologies]

    def create_projects(self, technologies):
        projects = [
            {
                "title": "E-Commerce Platform",
                "short_description": "A fully-featured e-commerce platform with product catalog, shopping cart, and payment processing.",
                "description": "Built a complete e-commerce solution using Django and PostgreSQL. The platform includes user authentication, product management, shopping cart functionality, and integration with multiple payment gateways. The frontend was developed with Tailwind CSS for responsive design.",
                "challenge": "The main challenge was integrating multiple payment gateways while ensuring PCI compliance and security. Additionally, the product catalog needed to handle thousands of products with various attributes and variations.",
                "solution": "Implemented a modular payment system that could easily add new payment methods. Used Django's class-based views and models to create a flexible product catalog that could scale with the business needs.",
                "results": "The platform successfully launched and handled over 10,000 transactions in its first month. Customer satisfaction improved by 40% due to the streamlined checkout process.",
                "client_name": "ShopEasy",
                "project_date": timezone.datetime(2022, 3, 15),
                "status": "completed",
                "live_url": "https://shop-easy.example.com",
                "github_url": "https://github.com/stevesatcheme/shop-easy",
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Task Management System",
                "short_description": "A collaborative task management application for teams.",
                "description": "Developed a task management application that allows teams to create, assign, and track tasks. Features include real-time updates, file attachments, comments, and notifications. Built with Django backend and a modern JavaScript frontend.",
                "challenge": "Real-time updates were essential for this application. The challenge was to implement this without using WebSockets to reduce complexity.",
                "solution": "Implemented polling with optimized queries to minimize database load. Used Django's caching framework to improve performance.",
                "results": "The application is now used by over 50 teams with an average of 200 tasks created daily. User feedback indicates a 30% improvement in team productivity.",
                "client_name": "TeamFlow",
                "project_date": timezone.datetime(2022, 9, 10),
                "status": "completed",
                "live_url": "https://teamflow.example.com",
                "github_url": "https://github.com/stevesatcheme/teamflow",
                "is_featured": True,
                "is_published": True,
            },
            {
                "title": "Portfolio Website",
                "short_description": "A professional portfolio website to showcase my work and skills.",
                "description": "This portfolio website was built from scratch using Django for the backend and Tailwind CSS for the frontend. It features dynamic content management, internationalization (English/French), and a clean, minimalist design.",
                "challenge": "Creating a content management system that was flexible enough to handle all the different types of content (projects, articles, skills, etc.) while keeping the code maintainable.",
                "solution": "Implemented a modular architecture with Django models organized by functionality. Used Django's class-based views and template inheritance to create reusable components.",
                "results": "The portfolio has received positive feedback for its design and functionality. It serves as both a showcase of my work and a demonstration of my technical skills.",
                "client_name": "Personal",
                "project_date": timezone.datetime(2023, 1, 1),
                "status": "completed",
                "live_url": "https://stevesatcheme.example.com",
                "github_url": "https://github.com/stevesatcheme/portfolio",
                "is_featured": True,
                "is_published": True,
            },
        ]
        
        created_projects = []
        for project in projects:
            p = Project.objects.create(**project)
            # Add some technologies to each project
            p.technologies.set(technologies[:3])
            created_projects.append(p)
        
        return created_projects

    def create_project_images(self, projects):
        # This is a placeholder - in a real implementation, you'd need to handle file uploads
        for i, project in enumerate(projects):
            ProjectImage.objects.create(
                project=project,
                caption=f"Screenshot {i+1}",
                display_order=i,
            )

    def create_categories_and_tags(self):
        categories = [
            {"name": "Django", "display_order": 1},
            {"name": "Python", "display_order": 2},
            {"name": "Web Development", "display_order": 3},
            {"name": "Tutorials", "display_order": 4},
        ]
        
        tags = [
            "django", "python", "web", "development", "tutorial", "backend", "frontend", "api",
        ]
        
        created_categories = [Category.objects.create(**cat) for cat in categories]
        created_tags = [Tag.objects.create(name=tag) for tag in tags]
        
        return created_categories, created_tags

    def create_articles(self, profile, categories, tags):
        articles = [
            {
                "title": "Getting Started with Django",
                "excerpt": "A comprehensive guide to setting up your first Django project.",
                "content": """
                <h2>Introduction</h2>
                <p>Django is a high-level Python web framework that enables rapid development of secure and maintainable websites.</p>
                
                <h2>Installation</h2>
                <p>First, make sure you have Python installed. Then you can install Django using pip:</p>
                <pre><code>pip install django</code></pre>
                
                <h2>Creating a Project</h2>
                <p>To create a new Django project, run:</p>
                <pre><code>django-admin startproject myproject</code></pre>
                
                <h2>Running the Development Server</h2>
                <p>Navigate to your project directory and run:</p>
                <pre><code>python manage.py runserver</code></pre>
                <p>This will start the development server on http://127.0.0.1:8000/</p>
                
                <h2>Conclusion</h2>
                <p>You now have a basic Django project running! The next step is to create your first app.</p>
                """,
                "author": profile,
                "category": categories[0],
                "status": "published",
                "published_at": timezone.datetime(2023, 2, 15),
                "reading_time": 8,
                "is_featured": True,
                "seo_title": "Getting Started with Django - A Beginner's Guide",
                "seo_description": "Learn how to set up your first Django project with this comprehensive beginner's guide.",
            },
            {
                "title": "Building RESTful APIs with Django REST Framework",
                "excerpt": "Learn how to create powerful APIs with Django REST Framework.",
                "content": """
                <h2>Introduction to DRF</h2>
                <p>Django REST Framework (DRF) is a powerful and flexible toolkit for building Web APIs.</p>
                
                <h2>Installation</h2>
                <p>Install DRF using pip:</p>
                <pre><code>pip install djangorestframework</code></pre>
                
                <h2>Creating a Serializer</h2>
                <p>Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes.</p>
                
                <h2>Creating Views</h2>
                <p>DRF provides several classes for creating API views. The most common are APIView, GenericAPIView, and ViewSets.</p>
                
                <h2>Setting Up URLs</h2>
                <p>Configure your URLs to route requests to your API views.</p>
                
                <h2>Conclusion</h2>
                <p>With DRF, you can quickly build powerful, standards-compliant APIs for your Django applications.</p>
                """,
                "author": profile,
                "category": categories[1],
                "status": "published",
                "published_at": timezone.datetime(2023, 3, 10),
                "reading_time": 12,
                "is_featured": True,
                "seo_title": "Building RESTful APIs with Django REST Framework",
                "seo_description": "Learn how to create powerful, standards-compliant APIs with Django REST Framework.",
            },
        ]
        
        for i, article in enumerate(articles):
            a = Article.objects.create(**article)
            # Add some tags
            a.tags.set(tags[:3])

    def create_testimonials(self):
        testimonials = [
            {
                "name": "John Doe",
                "position": "CEO",
                "company": "Tech Corp",
                "testimonial": "Steve is an exceptional developer. He delivered our project on time and exceeded all our expectations. Highly recommended!",
                "rating": 5,
                "is_featured": True,
                "display_order": 1,
            },
            {
                "name": "Jane Smith",
                "position": "CTO",
                "company": "Innovate Inc.",
                "testimonial": "Working with Steve was a great experience. His technical skills are impressive, and he's very professional in his approach.",
                "rating": 5,
                "is_featured": True,
                "display_order": 2,
            },
        ]
        for testimonial in testimonials:
            Testimonial.objects.create(**testimonial)

    def create_seo(self):
        seo_data = [
            {
                "page": "home",
                "seo_title": "Steve Satcheme | Full-Stack Developer & Digital Solutions Builder",
                "seo_description": "Professional portfolio of Steve Satcheme, Full-Stack Developer specializing in Django, Python, and modern web technologies.",
            },
            {
                "page": "about",
                "seo_title": "About Steve Satcheme | Full-Stack Developer",
                "seo_description": "Learn more about Steve Satcheme, his background, skills, and professional experience.",
            },
            {
                "page": "services",
                "seo_title": "Services | Steve Satcheme",
                "seo_description": "Professional web development services including Django development, API creation, and technical consulting.",
            },
        ]
        for seo in seo_data:
            SEO.objects.create(**seo)