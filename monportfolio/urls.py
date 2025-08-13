# monportfolio/urls.py
from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLogoutView, HomeView, ProfilView, ProjetListView, ProjetDetailView, ArticleListView,
    ArticleDetailView, AProposView, ContactView, ProjetListAPI, ArticleListAPI, LoginView
)

app_name = 'monportfolio'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profil/', ProfilView.as_view(), name='profil'),
    path('projets/', ProjetListView.as_view(), name='projet_list'),
    path('projets/<uuid:pk>/', ProjetDetailView.as_view(), name='projet_detail'),
    
    path('projets/', ProjetListView.as_view(), name='projets'),
    
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<uuid:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('articles/', ArticleListView.as_view(), name='articles'),
    path('a-propos/', AProposView.as_view(), name='a_propos'),
    path('contact/', ContactView.as_view(), name='contact'), 
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),   
    path('api/projets/', ProjetListAPI.as_view(), name='projet_list_api'),
    path('api/articles/', ArticleListAPI.as_view(), name='article_list_api'),
]
