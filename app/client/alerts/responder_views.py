from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import logging

from .models import ResponseUnit, Alert, AlertStatus, UnitStatus

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
            # Transition: EN_ROUTE/ON_SCENE → AVAILABLE
            if user_unit.status == UnitStatus.EN_ROUTE or user_unit.status == UnitStatus.ON_SCENE:
                user_unit.status = UnitStatus.AVAILABLE
                active_alert.status = AlertStatus.RESOLVED
                user_unit.save()
                active_alert.save()
                logger.info(f"Unit {user_unit.unit_name} completed alert {active_alert.alert_id} by {request.user.username}")
                messages.success(request, 'Alert marked as COMPLETE')
        
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)
        
        # Redirect back to dashboard
        return redirect('responder_dashboard')
        
    except Exception as e:
        logger.error(f"Error updating unit status: {str(e)}")
        messages.error(request, f'Error updating status: {str(e)}')
        return redirect('responder_dashboard')
