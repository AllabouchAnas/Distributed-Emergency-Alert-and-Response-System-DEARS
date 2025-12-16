from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('declare/', views.declare_emergency, name='declare'),
    path('status/<uuid:report_id>/', views.status_check, name='status'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update-status/', views.update_status, name='update_status'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
]
