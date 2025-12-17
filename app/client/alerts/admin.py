from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import EmergencyReport, UserProfile, Zone, ResponseUnit, Alert, Response


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role', 'assigned_unit', 'phone_number', 'address', 'city')


class UserAdmin(BaseUserAdmin):
    """Extended User admin with profile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'profile__role')
    
    def get_role(self, obj):
        """Display user role from profile."""
        return obj.profile.get_role_display() if hasattr(obj, 'profile') else 'N/A'
    
    get_role.short_description = 'Role'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles."""
    list_display = ('user', 'role', 'phone_number', 'city', 'created_at')
    list_filter = ('role', 'city', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Role', {
            'fields': ('role',)
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'address', 'city')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmergencyReport)
class EmergencyReportAdmin(admin.ModelAdmin):
    """Admin interface for Emergency Reports."""
    
    list_display = ('short_id', 'emergency_type', 'get_reporter_name', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'emergency_type', 'created_at')
    search_fields = ('reported_by__username', 'reported_by__first_name', 'reported_by__last_name', 
                     'description', 'location', 'id')
    readonly_fields = ('id', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Report Information', {
            'fields': ('id', 'status')
        }),
        ('Reporter', {
            'fields': ('reported_by',)
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
    
    def get_reporter_name(self, obj):
        """Display reporter's full name."""
        return obj.reported_by.get_full_name() or obj.reported_by.username
    
    get_reporter_name.short_description = 'Reporter'
    
    ordering = ('-created_at',)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    """Admin interface for Zones."""
    list_display = ('zone_name', 'description')
    search_fields = ('zone_name', 'description')


@admin.register(ResponseUnit)
class ResponseUnitAdmin(admin.ModelAdmin):
    """Admin interface for Response Units."""
    list_display = ('unit_name', 'unit_type', 'status', 'current_location', 'updated_at')
    list_filter = ('unit_type', 'status')
    search_fields = ('unit_name', 'current_location', 'contact_info')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Unit Information', {
            'fields': ('unit_name', 'unit_type', 'status')
        }),
        ('Location', {
            'fields': ('current_location',)
        }),
        ('Contact', {
            'fields': ('contact_info',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """Admin interface for Alerts."""
    list_display = ('id', 'emergency_type', 'get_user_name', 'status', 'location', 'created_at')
    list_filter = ('status', 'emergency_type', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('id', 'status')
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Emergency Details', {
            'fields': ('emergency_type', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude', 'zone')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        """Display user's full name."""
        return obj.user.get_full_name() or obj.user.username
    
    get_user_name.short_description = 'User'
    
    ordering = ('-created_at',)


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    """Admin interface for Responses."""
    list_display = ('id', 'get_alert_info', 'response_unit', 'status', 'assigned_at', 'completed_at')
    list_filter = ('status', 'assigned_at')
    search_fields = ('response_unit__unit_name', 'alert__id', 'notes')
    readonly_fields = ('assigned_at',)
    
    fieldsets = (
        ('Response Information', {
            'fields': ('alert', 'response_unit', 'status')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timeline', {
            'fields': ('assigned_at', 'arrived_at', 'completed_at')
        }),
    )
    
    def get_alert_info(self, obj):
        """Display alert information."""
        return f"Alert #{obj.alert.id} - {obj.alert.get_emergency_type_display()}"
    
    get_alert_info.short_description = 'Alert'
    
    ordering = ('-assigned_at',)
