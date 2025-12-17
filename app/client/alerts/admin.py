from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import EmergencyReport, UserProfile


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('role', 'phone_number', 'address', 'city')


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
