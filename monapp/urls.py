# monapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste_produits, name='liste_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('saisie-informations/', views.saisie_informations, name='saisie_informations'),
    path('supprimer/<int:pk>/', views.supprimer_produit, name='supprimer_produit'),
    path('generer-pdf/', views.GenererPDF.as_view(), name='generer_pdf'),

]
