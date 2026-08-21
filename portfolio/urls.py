from django.urls import path
from portfolio.views import (
    home_view,
    about_view,
    services_view,
    service_detail_view,
    projects_view,
    project_detail_view,
    experience_view,
    blog_view,
    article_detail_view,
    contact_view,
    search_view,
    resume_view,
    skills_view,
)

app_name = "portfolio"

urlpatterns = [
    path("", home_view, name="home"),
    path("about/", about_view, name="about"),
    path("services/", services_view, name="services"),
    path("services/<slug:slug>/", service_detail_view, name="service_detail"),
    path("projects/", projects_view, name="projects"),
    path("projects/<slug:slug>/", project_detail_view, name="project_detail"),
    path("experience/", experience_view, name="experience"),
    path("blog/", blog_view, name="blog"),
    path("blog/<slug:slug>/", article_detail_view, name="article_detail"),
    path("contact/", contact_view, name="contact"),
    path("search/", search_view, name="search"),
    path("resume/", resume_view, name="resume"),
    path("skills/", skills_view, name="skills"),
]