from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
import logging

from .models import EmergencyReport
from .forms import EmergencyReportForm, ReportSearchForm
from .services import send_alert_to_dispatcher

logger = logging.getLogger(__name__)


def home(request):
    """Home page with system overview and action buttons."""
    return render(request, 'home.html')


def declare_emergency(request):
    """Emergency declaration form view."""
    if request.method == 'POST':
        form = EmergencyReportForm(request.POST)
        
        if form.is_valid():
            # Save the report
            report = form.save()
            
            # Prepare data for dispatcher
            alert_data = {
                'id': report.id,
                'name': report.name,
                'contact_info': report.contact_info,
                'emergency_type': report.emergency_type,
                'location': report.location,
                'latitude': report.latitude,
                'longitude': report.longitude,
                'description': report.description,
            }
            
            # Send to dispatcher service
            success, message = send_alert_to_dispatcher(alert_data)
            
            if success:
                messages.success(request, 'Emergency alert submitted successfully! Help is on the way.')
            else:
                messages.warning(request, f'Alert saved locally. {message}')
            
            # Redirect to status page
            return redirect('status', report_id=report.id)
    else:
        form = EmergencyReportForm()
    
    return render(request, 'declare.html', {'form': form})


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
    """Admin dashboard for managing all emergency reports."""
    # Get filter parameter
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset
    reports = EmergencyReport.objects.all()
    
    # Apply filters
    if status_filter and status_filter != 'all':
        reports = reports.filter(status=status_filter)
    
    # Get statistics
    stats = {
        'total': EmergencyReport.objects.count(),
        'active': EmergencyReport.objects.filter(status=EmergencyReport.NEW).count(),
        'in_progress': EmergencyReport.objects.filter(status=EmergencyReport.IN_PROGRESS).count(),
        'resolved': EmergencyReport.objects.filter(status=EmergencyReport.RESOLVED).count(),
    }
    
    context = {
        'reports': reports,
        'stats': stats,
        'current_filter': status_filter,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
@require_POST
def update_status(request):
    """HTMX endpoint to update report status."""
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
        
        logger.info(f"Report {report_id} status updated to {new_status}")
        
        # Return updated table row HTML
        return render(request, 'partials/report_row.html', {'report': report})
        
    except EmergencyReport.DoesNotExist:
        return JsonResponse({'error': 'Report not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating report status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


class CustomLoginView(LoginView):
    """Custom login view with DEARS styling."""
    template_name = 'login.html'
    redirect_authenticated_user = True
