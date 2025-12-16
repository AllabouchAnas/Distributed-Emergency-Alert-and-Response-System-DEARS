from django.contrib import admin
from .models import EmergencyReport


@admin.register(EmergencyReport)
class EmergencyReportAdmin(admin.ModelAdmin):
    """Admin interface for Emergency Reports."""
    
    list_display = ('short_id', 'emergency_type', 'name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'emergency_type', 'created_at')
    search_fields = ('name', 'description', 'location', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('id', 'status')
        }),
        ('Reporter Details', {
            'fields': ('name', 'contact_info')
        }),
        ('Emergency Details', {
            'fields': ('emergency_type', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def short_id(self, obj):
        """Display shortened ID in list view."""
        return str(obj.id)[:8]
    
    short_id.short_description = 'Report ID'
    
    ordering = ('-created_at',)
