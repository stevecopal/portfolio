from django.urls import path
from portfolio.views import (
    home_view,
    services_view,
    service_detail_view,
    experience_view,
    projects_view,
    project_detail_view,
    contact_view,
)

app_name = "portfolio"

urlpatterns = [
    path("", home_view, name="home"),
    path("solutions/", services_view, name="services"),
    path("solutions/<slug:slug>/", service_detail_view, name="service_detail"),
    path("experience/", experience_view, name="experience"),
    path("work/", projects_view, name="projects"),
    path("work/<slug:slug>/", project_detail_view, name="project_detail"),
    path("contact/", contact_view, name="contact"),
]
