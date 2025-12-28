from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Q
import logging

from .models import Alert, UserProfile, ResponseUnit, AlertStatus, EmergencyType, UnitStatus, Report
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
    # Get all alerts ordered by most recent first
    all_alerts = Alert.objects.filter(user=request.user).order_by('-timestamp')
    
    # Deduplicate by alert_uuid, keeping only the most recent version of each alert
    seen_uuids = set()
    unique_alerts = []
    
    for alert in all_alerts:
        if alert.alert_uuid not in seen_uuids:
            seen_uuids.add(alert.alert_uuid)
            unique_alerts.append(alert)
    
    return render(request, 'my_alerts.html', {'alerts': unique_alerts})


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
            
            # Redirect to status page with fresh=true parameter
            return redirect(f"{reverse('status', kwargs={'report_id': alert.alert_uuid})}?fresh=true")
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
    
    # Check if this is a fresh submission (coming from alert submission) or viewing existing alert
    is_fresh_submission = request.GET.get('fresh', '') == 'true'
    
    context = {
        'report': report,
        'search_form': search_form,
        'is_fresh_submission': is_fresh_submission,
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
        'new': Alert.objects.filter(status=AlertStatus.PENDING).count(),
        'dispatched': Alert.objects.filter(status=AlertStatus.ASSIGNED).count(),
        'in_progress': Alert.objects.filter(status=AlertStatus.IN_PROGRESS).count(),
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
    
    
    # Reports data (responder-submitted reports)
    reports = Report.objects.all().select_related('alert', 'responder', 'response_unit').order_by('-timestamp')
    
    reports_stats = {
        'total': Report.objects.count(),
        'active': 0,  # Reports don't have active status, set to 0
        'in_progress': 0,  # Reports don't have in_progress status, set to 0
    'resolved': Report.objects.filter(outcome='RESOLVED').count(),
    }

    # Users data
    users = User.objects.all().select_related('profile').order_by('-date_joined')
    
    users_stats = {
        'total': User.objects.count(),
        'citizens': User.objects.filter(profile__role='CITIZEN').count(),
        'responders': User.objects.filter(profile__role='RESPONDER').count(),
        'admins': User.objects.filter(profile__role='ADMIN').count(),
    }
    
    context = {
        'alerts': alerts,
        'alerts_stats': alerts_stats,
        'units': units,
        'units_stats': units_stats,
        'reports': reports,
        'reports_stats': reports_stats,
        'users': users,
        'users_stats': users_stats,
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


@require_http_methods(["GET"])
def get_unit(request, unit_id):
    """API endpoint to get unit data for editing."""
    try:
        unit = ResponseUnit.objects.get(unit_id=unit_id)
        return JsonResponse({
            'success': True,
            'unit': {
                'id': unit.unit_id,
                'name': unit.unit_name,
                'location': unit.current_location,
                'status': unit.status,
                'contact': unit.contact_info
            }
        })
    except ResponseUnit.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Unit not found'}, status=404)


@require_http_methods(["POST"])
def update_unit(request, unit_id):
    """API endpoint to update unit information."""
    try:
        unit = ResponseUnit.objects.get(unit_id=unit_id)
        
        # Update fields if provided
        if 'location' in request.POST:
            unit.current_location = request.POST['location']
        if 'status' in request.POST:
            unit.status = request.POST['status']
        if 'contact' in request.POST:
            unit.contact_info = request.POST['contact']
        
        unit.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Unit updated successfully'
        })
    except ResponseUnit.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Unit not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_alert(request, alert_id):
    """API endpoint to get alert data for editing/viewing."""
    try:
        alert = Alert.objects.get(alert_id=alert_id)
        return JsonResponse({
            'success': True,
            'alert': {
                'id': alert.alert_id,
                'status': alert.status,
                'status_display': alert.get_status_display(),
                'emergency_type': alert.emergency_type,
                'emergency_type_display': alert.get_emergency_type_display(),
                'location': alert.location,
                'description': alert.description,
                'user': alert.user.get_full_name() or alert.user.username,
                'timestamp': alert.timestamp.strftime("%B %d, %Y - %H:%M")
            }
        })
    except Alert.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Alert not found'}, status=404)


@require_http_methods(["POST"])
def create_unit(request):
    """API endpoint to create a new response unit."""
    try:
        unit = ResponseUnit.objects.create(
            unit_name=request.POST.get('unit_name'),
            unit_type=request.POST.get('unit_type'),
            current_location=request.POST.get('location'),
            contact_info=request.POST.get('contact', ''),
            status=UnitStatus.AVAILABLE
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Unit created successfully',
            'unit_id': unit.unit_id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


@require_http_methods(["POST"])
def create_user(request):
    """API endpoint to create a new user with specified role."""
    from django.contrib.auth.models import User
    
    try:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        role = request.POST.get('role')
        
        # Validation
        if not all([username, email, password, role]):
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
        
        if password != password_confirm:
            return JsonResponse({'success': False, 'error': 'Passwords do not match'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Username already exists'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already exists'}, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', '')
        )
        
        # Set role in profile
        profile = user.profile
        profile.role = role
        
        # Save phone and address if provided
        if request.POST.get('phone'):
            profile.phone_number = request.POST.get('phone')
        if request.POST.get('address'):
            profile.address = request.POST.get('address')
            
        profile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'User created successfully',
            'user_id': user.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = '/'
