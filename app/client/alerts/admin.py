from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, ResponseUnit, Alert


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
        return obj.profile.role if hasattr(obj, 'profile') else 'N/A'
    
    get_role.short_description = 'Role'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for User Profiles."""
    list_display = ('user', 'role', 'phone_number', 'city')
    list_filter = ('role', 'city')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    
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
    )


@admin.register(ResponseUnit)
class ResponseUnitAdmin(admin.ModelAdmin):
    """Admin interface for Response Units."""
    list_display = ('unit_name', 'unit_type', 'status', 'current_location')
    list_filter = ('unit_type', 'status')
    search_fields = ('unit_name', 'current_location')
    
    fieldsets = (
        ('Unit Information', {
            'fields': ('unit_name', 'unit_type', 'status')
        }),
        ('Location', {
            'fields': ('current_location', 'latitude', 'longitude')
        }),
    )


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """Admin interface for Alerts."""
    list_display = ('alert_id', 'emergency_type', 'get_user_name', 'status', 'location', 'timestamp')
    list_filter = ('status', 'emergency_type', 'timestamp')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'description', 'location')
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('status',)
        }),
        ('User', {
            'fields': ('user',)
        }),
        ('Emergency Details', {
            'fields': ('emergency_type', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Assignment', {
            'fields': ('assigned_unit',)
        }),
        ('Timestamps', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    def get_user_name(self, obj):
        """Display user's full name."""
        return obj.user.get_full_name() or obj.user.username
    
    get_user_name.short_description = 'User'
    
    ordering = ('-timestamp',)
