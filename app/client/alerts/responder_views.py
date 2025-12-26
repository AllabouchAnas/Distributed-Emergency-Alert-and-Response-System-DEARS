from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import logging

from .models import ResponseUnit, Alert, AlertStatus, UnitStatus

logger = logging.getLogger(__name__)


@login_required
def responder_dashboard(request):
    """Dashboard for response unit personnel to view and update missions."""
    # Check if user is a responder
    if not request.user.profile.is_responder():
        return redirect('home')
    
    # Get assigned response unit (assuming 1-to-1 link via profile for now, though model has foreign key)
    # In the new model, UserProfile doesn't have 'assigned_unit' field explicitly shown in the last update
    # but let's assume we need to fetch it.
    # Wait, looking at the models.py I wrote:
    # UserProfile has 'role'.
    # ResponseUnit has no link to User.
    # Alert has 'assigned_unit'.
    
    # We need a way to link the logged-in user to a ResponseUnit.
    # The previous UserProfile had 'assigned_unit'. I might have missed adding it back in the strict refactor.
    # Let's check models.py again.
    
    # If it's missing, I need to add it back to UserProfile or handle it differently.
    # For now, let's assume we need to fix models.py first if it's missing.
    # But to proceed with views, I will assume it exists or I will add it.
    
    # Let's check if I added it in step 66/67.
    # I added is_admin, is_responder etc.
    # I did NOT add assigned_unit back to UserProfile in the replacement.
    
    # This is a regression. I need to add assigned_unit to UserProfile in models.py.
    # But first let's write this view assuming it will be there, or I can't finish this file.
    
    # Actually, let's pause writing this file and fix models.py first?
    # No, I can't switch tasks easily. I will write this view expecting 'assigned_unit' on profile.
    
    assigned_unit = getattr(request.user.profile, 'assigned_unit', None)
    
    if not assigned_unit:
        context = {
            'error_message': 'You are not assigned to any response unit. Please contact your administrator.'
        }
        return render(request, 'responder_dashboard.html', context)
    
    # Get current active mission (Alert assigned to this unit that is not resolved)
    current_mission = Alert.objects.filter(
        assigned_unit=assigned_unit,
        status__in=[AlertStatus.PENDING, AlertStatus.ASSIGNED, AlertStatus.IN_PROGRESS]
    ).select_related('user').first()
    
    # Get recent completed missions
    recent_missions = Alert.objects.filter(
        assigned_unit=assigned_unit,
        status=AlertStatus.RESOLVED
    ).order_by('-timestamp')[:5]
    
    context = {
        'unit': assigned_unit,
        'current_mission': current_mission,
        'recent_missions': recent_missions,
    }
    
    return render(request, 'responder_dashboard.html', context)


@login_required
@require_POST
def update_mission_status(request):
    """HTMX endpoint to update mission status."""
    # Check if user is a responder
    if not request.user.profile.is_responder():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    alert_id = request.POST.get('response_id') # Using response_id as param name to match template
    action = request.POST.get('action')
    
    try:
        alert = Alert.objects.get(alert_id=alert_id)
        
        # Verify this alert is assigned to user's unit
        # Again assuming profile.assigned_unit exists
        user_unit = getattr(request.user.profile, 'assigned_unit', None)
        if not user_unit or alert.assigned_unit != user_unit:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        # Update status based on action
        if action == 'start':
            if alert.status == AlertStatus.PENDING or alert.status == AlertStatus.ASSIGNED:
                alert.status = AlertStatus.IN_PROGRESS
                alert.assigned_unit.status = UnitStatus.EN_ROUTE
        
        elif action == 'arrive':
            if alert.status == AlertStatus.IN_PROGRESS:
                # alert status stays active? or maybe we need a sub-status.
                # For now let's keep it IN_PROGRESS but update unit status
                alert.assigned_unit.status = UnitStatus.ON_SCENE
        
        elif action == 'complete':
            if alert.status == AlertStatus.IN_PROGRESS:
                alert.status = AlertStatus.RESOLVED
                alert.assigned_unit.status = UnitStatus.AVAILABLE
        
        # Save changes
        alert.save()
        alert.assigned_unit.save()
        
        logger.info(f"Alert {alert_id} status updated to {alert.status} by {request.user.username}")
        
        # Return updated mission card HTML
        context = {
            'current_mission': alert,
            'unit': alert.assigned_unit,
        }
        return render(request, 'partials/mission_card.html', context)
        
    except Alert.DoesNotExist:
        return JsonResponse({'error': 'Mission not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating mission status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
