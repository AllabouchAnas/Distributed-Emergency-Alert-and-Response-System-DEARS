from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import logging

from .models import ResponseUnit, Alert, AlertStatus, UnitStatus, Report, ReportOutcome

logger = logging.getLogger(__name__)


@login_required
def responder_dashboard(request):
    """Minimal dashboard for response unit personnel to view and update their active alert."""
    # Check if user is a responder
    if not request.user.profile.is_responder():
        messages.error(request, 'Access denied. Responder privileges required.')
        return redirect('home')
    
    # Get assigned response unit from user profile
    assigned_unit = getattr(request.user.profile, 'assigned_unit', None)
    
    if not assigned_unit:
        context = {
            'error_message': 'You are not assigned to any response unit. Please contact your administrator.'
        }
        return render(request, 'responder_dashboard_minimal.html', context)
    
    # Get ONE active alert assigned to this unit (ASSIGNED or IN_PROGRESS status)
    active_alert = Alert.objects.filter(
        assigned_unit=assigned_unit,
        status__in=[AlertStatus.ASSIGNED, AlertStatus.IN_PROGRESS]
    ).select_related('user').first()
    
    context = {
        'unit': assigned_unit,
        'active_alert': active_alert,
    }
    
    return render(request, 'responder_dashboard_minimal.html', context)


@login_required
@require_POST
def update_unit_status(request):
    """API endpoint to update unit status based on responder actions."""
    # Check if user is a responder
    if not request.user.profile.is_responder():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    action = request.POST.get('action')
    
    try:
        # Get user's assigned unit
        user_unit = getattr(request.user.profile, 'assigned_unit', None)
        if not user_unit:
            return JsonResponse({'error': 'No unit assigned'}, status=400)
        
        # Get active alert for this unit
        active_alert = Alert.objects.filter(
            assigned_unit=user_unit,
            status__in=[AlertStatus.ASSIGNED, AlertStatus.IN_PROGRESS]
        ).first()
        
        if not active_alert:
            return JsonResponse({'error': 'No active alert found'}, status=400)
        
        # Update status based on action
        if action == 'on_scene':
            # Transition: AVAILABLE → ON_SCENE
            if user_unit.status == UnitStatus.AVAILABLE or active_alert.status == AlertStatus.ASSIGNED:
                user_unit.status = UnitStatus.ON_SCENE
                active_alert.status = AlertStatus.IN_PROGRESS
                user_unit.save()
                active_alert.save()
                logger.info(f"Unit {user_unit.unit_name} status updated to ON_SCENE by {request.user.username}")
                messages.success(request, 'Status updated to ON SCENE')
        
        elif action == 'complete':
            # Redirect to report form (unit stays ON_SCENE)
            if user_unit.status == UnitStatus.ON_SCENE:
                # Store alert ID in session for report form
                request.session['pending_report_alert_id'] = active_alert.alert_id
                return redirect('submit_report')
            else:
                messages.error(request, 'Unit must be ON SCENE to complete alert')
                return redirect('responder_dashboard')
        
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        # Redirect back to dashboard
        return redirect('responder_dashboard')
        
    except Exception as e:
        logger.error(f"Error updating unit status: {str(e)}")
        messages.error(request, f'Error updating status: {str(e)}')
        return redirect('responder_dashboard')


@login_required
def submit_report(request):
    """Display report form and handle report submission."""
    if not request.user.profile.is_responder():
        messages.error(request, 'Access denied. Responder privileges required.')
        return redirect('home')
    
    # Get alert ID from session
    alert_id = request.session.get('pending_report_alert_id')
    if not alert_id:
        messages.error(request, 'No pending report found')
        return redirect('responder_dashboard')
    
    try:
        alert = Alert.objects.get(alert_id=alert_id)
        user_unit = request.user.profile.assigned_unit
        
        if request.method == 'POST':
            # Get form data
            description = request.POST.get('description', '').strip()
            actions_taken = request.POST.get('actions_taken', '').strip()
            outcome = request.POST.get('outcome', ReportOutcome.RESOLVED)
            notes = request.POST.get('notes', '').strip()
            
            # Validate required fields
            if not description or not actions_taken:
                messages.error(request, 'Description and Actions Taken are required')
                return render(request, 'submit_report.html', {'alert': alert})
            
            # Create report
            Report.objects.create(
                alert=alert,
                responder=request.user,
                response_unit=user_unit,
                description=description,
                actions_taken=actions_taken,
                outcome=outcome,
                notes=notes
            )
            
            # Update alert and unit status
            alert.status = AlertStatus.RESOLVED
            alert.save()
            
            user_unit.status = UnitStatus.AVAILABLE
            user_unit.save()
            
            # Clear session
            del request.session['pending_report_alert_id']
            
            logger.info(f"Report submitted for alert {alert_id} by {request.user.username}")
            messages.success(request, 'Report submitted successfully')
            return redirect('responder_dashboard')
        
        # GET request - display form
        context = {
            'alert': alert,
            'unit': user_unit,
            'outcome_choices': ReportOutcome.choices
        }
        return render(request, 'submit_report.html', context)
        
    except Alert.DoesNotExist:
        messages.error(request, 'Alert not found')
        return redirect('responder_dashboard')
    except Exception as e:
        logger.error(f"Error submitting report: {str(e)}")
        messages.error(request, f'Error submitting report: {str(e)}')
        return redirect('responder_dashboard')


@login_required
def view_report(request, report_id):
    """Display full report details."""
    try:
        report = Report.objects.select_related('alert', 'responder', 'response_unit').get(report_id=report_id)
        
        context = {
            'report': report,
        }
        return render(request, 'view_report.html', context)
        
    except Report.DoesNotExist:
        messages.error(request, 'Report not found')
        return redirect('dashboard')
