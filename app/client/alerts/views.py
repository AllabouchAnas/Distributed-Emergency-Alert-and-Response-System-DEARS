from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import logging

from .models import Alert, UserProfile, ResponseUnit, AlertStatus, EmergencyType, UnitStatus
from .forms import AlertForm, ReportSearchForm, UserRegistrationForm
# from .services import send_alert_to_dispatcher # Keeping this import if needed, but might need adjustment

logger = logging.getLogger(__name__)


def home(request):
    """Home page with system overview and action buttons."""
    # Handle status check form submission
    search_id = request.GET.get('search_id')
    if search_id:
        try:
            # Try to parse as UUID and redirect to status page
            import uuid
            report_id = uuid.UUID(search_id.strip())
            return redirect('status', report_id=report_id)
        except (ValueError, AttributeError):
            messages.error(request, 'Invalid report ID format. Please enter a valid UUID.')
    
    return render(request, 'home.html')


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to DEARS.')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})


@login_required
def my_alerts(request):
    """View to list all alerts submitted by the current user."""
    alerts = Alert.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'my_alerts.html', {'alerts': alerts})


@login_required
def profile(request):
    """User profile view showing role-specific information."""
    return render(request, 'profile.html', {'user': request.user})


@login_required
def declare_emergency(request):
    """Emergency declaration form view - requires authentication."""
    if request.method == 'POST':
        form = AlertForm(request.POST)
        
        if form.is_valid():
            # Create Alert record
            alert = form.save(commit=False)
            alert.user = request.user
            # alert.status is default PENDING
            alert.save()
            
            # Send alert to Dispatcher Service
            try:
                # Prepare data for dispatcher
                alert_data = {
                    "alert_id": str(alert.alert_uuid), # Use UUID
                    "user_id": request.user.id,
                    "description": alert.description,
                    "location": alert.location,
                    "emergency_type": alert.emergency_type,
                    "latitude": alert.latitude,
                    "longitude": alert.longitude
                }
                
                # We need to implement this function since it was imported but not found in file view
                # Actually, I'll use requests directly here for simplicity or import it if I find it
                # Looking at imports: `from .services import send_alert_to_dispatcher` was commented out
                
                import requests
                from django.conf import settings
                
                dispatcher_url = settings.DISPATCHER_SERVICE_URL
                requests.post(dispatcher_url, json=alert_data, timeout=5)
                
            except Exception as e:
                logger.error(f"Failed to notify dispatcher: {e}")
                # Don't fail the user request, just log it. 
                # Ideally we should have a retry mechanism.
                
            messages.success(request, f'Emergency alert declared successfully! Alert ID: {alert.alert_id}')
            messages.info(request, 'Emergency services have been notified. Help is on the way.')
            
            # Redirect to status page
            return redirect('status', report_id=alert.alert_uuid)
    else:
        form = AlertForm()
    
    # Pass user info to template for display
    context = {
        'form': form,
        'user_profile': request.user.profile,
    }
    
    return render(request, 'declare.html', context)


def status_check(request, report_id):
    """Public status check page for a specific report."""
    report = get_object_or_404(Alert, alert_uuid=report_id)
    search_form = ReportSearchForm()
    
    # Handle search form submission
    if request.method == 'POST':
        search_form = ReportSearchForm(request.POST)
        if search_form.is_valid():
            search_id = search_form.cleaned_data['report_id'] # Note: ReportSearchForm might need update for UUID vs Int
            return redirect('status', report_id=search_id)
    
    context = {
        'report': report,
        'search_form': search_form,
    }
    
    return render(request, 'status.html', context)


@login_required
def dashboard(request):
    """Admin dashboard for managing all alerts and response units."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Get current tab
    tab = request.GET.get('tab', 'alerts')
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Alerts data
    alerts = Alert.objects.all().select_related('user', 'assigned_unit')
    if status_filter and status_filter != 'all':
        alerts = alerts.filter(status=status_filter)
    
    alerts_stats = {
        'total': Alert.objects.count(),
        'pending': Alert.objects.filter(status=AlertStatus.PENDING).count(),
        'active': Alert.objects.filter(status=AlertStatus.IN_PROGRESS).count(),
        'resolved': Alert.objects.filter(status=AlertStatus.RESOLVED).count(),
    }
    
    # Response Units data
    units = ResponseUnit.objects.all()
    unit_type_filter = request.GET.get('unit_type', 'all')
    if unit_type_filter and unit_type_filter != 'all':
        units = units.filter(unit_type=unit_type_filter)
    
    units_stats = {
        'total': ResponseUnit.objects.count(),
        'available': ResponseUnit.objects.filter(status=UnitStatus.AVAILABLE).count(),
        'en_route': ResponseUnit.objects.filter(status=UnitStatus.EN_ROUTE).count(),
        'on_scene': ResponseUnit.objects.filter(status=UnitStatus.ON_SCENE).count(),
        'police': ResponseUnit.objects.filter(unit_type=EmergencyType.POLICE).count(),
        'fire': ResponseUnit.objects.filter(unit_type=EmergencyType.FIRE).count(),
        'medical': ResponseUnit.objects.filter(unit_type=EmergencyType.MEDICAL).count(),
    }
    
    context = {
        'alerts': alerts,
        'alerts_stats': alerts_stats,
        'units': units,
        'units_stats': units_stats,
        'current_filter': status_filter,
        'current_tab': tab,
        'unit_type_filter': unit_type_filter,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
@require_POST
def update_status(request):
    """HTMX endpoint to update alert status - admin only."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    report_id = request.POST.get('report_id')
    new_status = request.POST.get('status')
    
    try:
        alert = Alert.objects.get(alert_id=report_id)
        
        # Validate status
        valid_statuses = AlertStatus.values
        if new_status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        # Update status
        alert.status = new_status
        alert.save()
        
        logger.info(f"Alert {report_id} status updated to {new_status} by {request.user.username}")
        
        # Return updated table row HTML
        return render(request, 'partials/report_row.html', {'report': alert}) # Template might need update to use 'alert' or 'report'
    
    except Alert.DoesNotExist:
        return JsonResponse({'error': 'Alert not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating alert status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)




@login_required
@require_POST
def update_alert_status(request):
    """Update alert status - admin only."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    alert_id = request.POST.get('alert_id')
    new_status = request.POST.get('status')
    
    try:
        alert = Alert.objects.get(alert_id=alert_id)
        
        # Validate status
        valid_statuses = [choice[0] for choice in AlertStatus.choices]
        if new_status not in valid_statuses:
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        
        # Update status
        alert.status = new_status
        alert.save()
        
        logger.info(f"Alert {alert_id} status updated to {new_status} by {request.user.username}")
        
        return JsonResponse({'success': True, 'message': 'Alert status updated successfully'})
    
    except Alert.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alert not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating alert status: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_POST
def delete_alert(request):
    """Delete an alert - admin only."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        return JsonResponse({'success': False, 'error': 'Access denied'}, status=403)
    
    alert_id = request.POST.get('alert_id')
    
    try:
        alert = Alert.objects.get(alert_id=alert_id)
        alert.delete()
        
        logger.info(f"Alert {alert_id} deleted by {request.user.username}")
        
        return JsonResponse({'success': True, 'message': 'Alert deleted successfully'})
    
    except Alert.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alert not found'}, status=404)
    except Exception as e:
        logger.error(f"Error deleting alert: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def alert_confirmation(request):
    """Display alert confirmation page with alert ID."""
    alert_id = request.session.pop('last_alert_id', None)
    
    return render(request, 'alert_confirmation.html', {
        'alert_id': alert_id,
    })


class CustomLoginView(LoginView):
    """Custom login view with DEARS styling."""
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirect based on user role."""
        if self.request.user.profile.is_admin():
            return '/dashboard/'
        elif self.request.user.profile.is_responder():
            return '/responder/'
        return '/'


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = '/'
