from django.urls import path
from . import views
from . import responder_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('declare/', views.declare_emergency, name='declare'),
    path('alert-confirmation/', views.alert_confirmation, name='alert_confirmation'),
    path('status/<uuid:report_id>/', views.status_check, name='status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-status/', views.update_status, name='update_status'),
    path('responder/', responder_views.responder_dashboard, name='responder_dashboard'),
    path('responder/update-mission/', responder_views.update_mission_status, name='update_mission_status'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
]
