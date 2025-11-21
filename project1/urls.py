# Fichiers de routage principal (dears_project/urls.py)

from django.contrib import admin
from django.urls import path
# Importez vos vues depuis l'application alert_manager
from alert_manager import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Étape 1: Sélection du type d'urgence (Page d'accueil)
    path('', views.select_emergency_type, name='select_type'),
    
    # Étape 2: Formulaire des détails de l'alerte
    # Le 'type' est passé dans l'URL (police, fire, medical)
    path('report/<str:alert_type>/', views.report_details_view, name='report_details'),
]