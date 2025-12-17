from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import logging

from .models import EmergencyReport, UserProfile
from .forms import EmergencyReportForm, ReportSearchForm, UserRegistrationForm
from .services import send_alert_to_dispatcher

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
def declare_emergency(request):
    """Emergency declaration form view - requires authentication."""
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        
        if form.is_valid():
            # Do NOT save EmergencyReport - only send to dispatcher
            # Prepare data for dispatcher
            alert_data = {
                'user_id': request.user.id,
                'emergency_type': form.cleaned_data['emergency_type'],
                'location': form.cleaned_data['location'],
                'description': form.cleaned_data['description'],
            }
            
            # Send to dispatcher service
            success, alert_id = send_alert_to_dispatcher(alert_data)
            
            if success and alert_id:
                # Create Alert record in local DB for tracking (optional)
                from .models import Alert
                alert = Alert.objects.create(
                    user=request.user,
                    emergency_type=form.cleaned_data['emergency_type'],
                    location=form.cleaned_data['location'],
                    latitude=form.cleaned_data.get('latitude'),
                    longitude=form.cleaned_data.get('longitude'),
                    description=form.cleaned_data['description'],
                    status=Alert.DISPATCHED
                )
                
                messages.success(request, f'Emergency alert dispatched successfully! Alert ID: {alert_id}')
                messages.info(request, 'Emergency services have been notified. Help is on the way.')
                
                # Redirect to status page
                return redirect('status', report_id=alert.id)
            else:
                messages.error(request, 'Failed to send emergency alert to dispatcher. Please try again or call emergency services directly.')
                # Stay on form
    else:
        form = EmergencyReportForm()
    
    # Pass user info to template for display
    context = {
        'form': form,
        'user_profile': request.user.profile,
    }
    
    return render(request, 'declare.html', context)


def status_check(request, report_id):
    """Public status check page for a specific report."""
    report = get_object_or_404(EmergencyReport, id=report_id)
    search_form = ReportSearchForm()
    
    # Handle search form submission
    if request.method == 'POST':
        search_form = ReportSearchForm(request.POST)
        if search_form.is_valid():
            search_id = search_form.cleaned_data['report_id']
            return redirect('status', report_id=search_id)
    
    context = {
        'report': report,
        'search_form': search_form,
    }
    
    return render(request, 'status.html', context)


@login_required
def dashboard(request):
    """Admin dashboard for managing all emergency reports, alerts, and response units."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('home')
    
    # Get current tab
    tab = request.GET.get('tab', 'reports')
    
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Emergency Reports data
    reports = EmergencyReport.objects.all().select_related('reported_by', 'reported_by__profile')
    if status_filter and status_filter != 'all':
        reports = reports.filter(status=status_filter)
    
    reports_stats = {
        'total': EmergencyReport.objects.count(),
        'active': EmergencyReport.objects.filter(status=EmergencyReport.NEW).count(),
        'in_progress': EmergencyReport.objects.filter(status=EmergencyReport.IN_PROGRESS).count(),
        'resolved': EmergencyReport.objects.filter(status=EmergencyReport.RESOLVED).count(),
    }
    
    # Alerts data
    from .models import Alert, ResponseUnit, Response
    alerts = Alert.objects.all().select_related('user', 'zone')
    if status_filter and status_filter != 'all':
        alerts = alerts.filter(status=status_filter)
    
    alerts_stats = {
        'total': Alert.objects.count(),
        'new': Alert.objects.filter(status=Alert.NEW).count(),
        'dispatched': Alert.objects.filter(status=Alert.DISPATCHED).count(),
        'in_progress': Alert.objects.filter(status=Alert.IN_PROGRESS).count(),
        'resolved': Alert.objects.filter(status=Alert.RESOLVED).count(),
    }
    
    # Response Units data
    units = ResponseUnit.objects.all()
    unit_type_filter = request.GET.get('unit_type', 'all')
    if unit_type_filter and unit_type_filter != 'all':
        units = units.filter(unit_type=unit_type_filter)
    
    units_stats = {
        'total': ResponseUnit.objects.count(),
        'available': ResponseUnit.objects.filter(status=ResponseUnit.AVAILABLE).count(),
        'en_route': ResponseUnit.objects.filter(status=ResponseUnit.EN_ROUTE).count(),
        'on_site': ResponseUnit.objects.filter(status=ResponseUnit.ON_SITE).count(),
        'police': ResponseUnit.objects.filter(unit_type=ResponseUnit.POLICE).count(),
        'fire': ResponseUnit.objects.filter(unit_type=ResponseUnit.FIRE).count(),
        'medical': ResponseUnit.objects.filter(unit_type=ResponseUnit.MEDICAL).count(),
    }
    
    # Active Responses
    active_responses = Response.objects.filter(
        status__in=[Response.ASSIGNED, Response.EN_ROUTE, Response.ON_SITE]
    ).select_related('alert', 'response_unit')
    
    context = {
        'reports': reports,
        'reports_stats': reports_stats,
        'alerts': alerts,
        'alerts_stats': alerts_stats,
        'units': units,
        'units_stats': units_stats,
        'active_responses': active_responses,
        'current_filter': status_filter,
        'current_tab': tab,
        'unit_type_filter': unit_type_filter,
    }
    
    return render(request, 'dashboard.html', context)



@login_required
@require_POST
def update_status(request):
    """HTMX endpoint to update report status - admin only."""
    # Check if user is admin
    if not request.user.profile.is_admin():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    report_id = request.POST.get('report_id')
    new_status = request.POST.get('status')
    
    try:
        report = EmergencyReport.objects.get(id=report_id)
        
        # Validate status
        valid_statuses = [choice[0] for choice in EmergencyReport.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return JsonResponse({'error': 'Invalid status'}, status=400)
        
        # Update status
        report.status = new_status
        report.save()
        
        logger.info(f"Report {report_id} status updated to {new_status} by {request.user.username}")
        
        # Return updated table row HTML
        return render(request, 'partials/report_row.html', {'report': report})
    
    except EmergencyReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating report status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)



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
