from django.urls import path
from . import views
from . import responder_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('declare_emergency/', views.declare_emergency, name='declare_emergency'),
    path('alert-confirmation/', views.alert_confirmation, name='alert_confirmation'),
    path('status/<int:report_id>/', views.status_check, name='status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-status/', views.update_status, name='update_status'),
    path('alerts/update-alert-status/', views.update_alert_status, name='update_alert_status'),
    path('alerts/delete-alert/', views.delete_alert, name='delete_alert'),
    path('responder/', responder_views.responder_dashboard, name='responder_dashboard'),
    path('responder/update-status/', responder_views.update_unit_status, name='update_unit_status'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
]
