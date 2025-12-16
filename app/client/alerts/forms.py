from django import forms
from .models import EmergencyReport


class EmergencyReportForm(forms.ModelForm):
    """Form for citizens to submit emergency reports."""
    
    class Meta:
        model = EmergencyReport
        fields = ['name', 'contact_info', 'emergency_type', 'location', 
                  'latitude', 'longitude', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your full name',
                'required': True,
            }),
            'contact_info': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Email or phone number',
                'required': True,
            }),
            'emergency_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Street address or landmark description',
                'required': True,
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 40.7128',
                'step': '0.000001',
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., -74.0060',
                'step': '0.000001',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Describe the emergency situation in detail...',
                'rows': 5,
                'required': True,
            }),
        }
        labels = {
            'name': 'Your Name',
            'contact_info': 'Contact Information',
            'emergency_type': 'Emergency Type',
            'location': 'Location Description',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'description': 'Emergency Description',
        }


class ReportSearchForm(forms.Form):
    """Form for searching reports by ID."""
    
    report_id = forms.UUIDField(
        label='Report ID',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter report ID (e.g., a1b2c3d4-...)',
        })
    )
