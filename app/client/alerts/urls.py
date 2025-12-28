from django.urls import path
from . import views
from . import responder_views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('declare_emergency/', views.declare_emergency, name='declare_emergency'),
    path('alert-confirmation/', views.alert_confirmation, name='alert_confirmation'),
    path('status/<uuid:report_id>/', views.status_check, name='status'),
    path('my-alerts/', views.my_alerts, name='my_alerts'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-status/', views.update_status, name='update_status'),
    path('alerts/update-alert-status/', views.update_alert_status, name='update_alert_status'),
    path('alerts/delete-alert/', views.delete_alert, name='delete_alert'),
    path('responder/', responder_views.responder_dashboard, name='responder_dashboard'),
    path('responder/update-status/', responder_views.update_unit_status, name='update_unit_status'),
    path('responder/submit-report/', responder_views.submit_report, name='submit_report'),
    path('responder/report/<int:report_id>/', responder_views.view_report, name='view_report'),
    path('alerts/get-unit/<int:unit_id>/', views.get_unit, name='get_unit'),
    path('alerts/update-unit/<int:unit_id>/', views.update_unit, name='update_unit'),
    path('alerts/get-alert/<int:alert_id>/', views.get_alert, name='get_alert'),
    path('alerts/create-unit/', views.create_unit, name='create_unit'),
    path('alerts/create-user/', views.create_user, name='create_user'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
]
