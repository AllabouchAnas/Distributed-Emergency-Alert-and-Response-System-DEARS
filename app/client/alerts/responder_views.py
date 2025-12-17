from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import logging

from .models import Response, ResponseUnit, Alert

logger = logging.getLogger(__name__)


@login_required
def responder_dashboard(request):
    """Dashboard for response unit personnel to view and update missions."""
    # Check if user is a responder
    if not request.user.profile.is_responder():
        return redirect('home')
    
    # Get assigned response unit
    assigned_unit = request.user.profile.assigned_unit
    
    if not assigned_unit:
        context = {
            'error_message': 'You are not assigned to any response unit. Please contact your administrator.'
        }
        return render(request, 'responder_dashboard.html', context)
    
    # Get current active mission (response in progress)
    current_mission = Response.objects.filter(
        response_unit=assigned_unit,
        status__in=[Response.ASSIGNED, Response.EN_ROUTE, Response.ON_SITE]
    ).select_related('alert', 'alert__user').first()
    
    # Get recent completed missions
    recent_missions = Response.objects.filter(
        response_unit=assigned_unit,
        status__in=[Response.COMPLETED, Response.CANCELLED]
    ).select_related('alert')[:5]
    
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
    
    response_id = request.POST.get('response_id')
    action = request.POST.get('action')
    
    try:
        response_obj = Response.objects.select_related('alert', 'response_unit').get(id=response_id)
        
        # Verify this response belongs to user's assigned unit
        if response_obj.response_unit != request.user.profile.assigned_unit:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        # Update status based on action
        if action == 'start':
            if response_obj.status == Response.ASSIGNED:
                response_obj.status = Response.EN_ROUTE
                response_obj.response_unit.status = ResponseUnit.EN_ROUTE
                response_obj.alert.status = Alert.IN_PROGRESS
        
        elif action == 'arrive':
            if response_obj.status == Response.EN_ROUTE:
                response_obj.status = Response.ON_SITE
                response_obj.response_unit.status = ResponseUnit.ON_SITE
                response_obj.arrived_at = timezone.now()
        
        elif action == 'complete':
            if response_obj.status == Response.ON_SITE:
                response_obj.status = Response.COMPLETED
                response_obj.completed_at = timezone.now()
                response_obj.response_unit.status = ResponseUnit.AVAILABLE
                response_obj.alert.status = Alert.RESOLVED
        
        # Save changes
        response_obj.save()
        response_obj.response_unit.save()
        response_obj.alert.save()
        
        logger.info(f"Response {response_id} status updated to {response_obj.status} by {request.user.username}")
        
        # Return updated mission card HTML
        context = {
            'current_mission': response_obj,
            'unit': response_obj.response_unit,
        }
        return render(request, 'partials/mission_card.html', context)
        
    except Response.DoesNotExist:
        return JsonResponse({'error': 'Mission not found'}, status=404)
    except Exception as e:
        logger.error(f"Error updating mission status: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
