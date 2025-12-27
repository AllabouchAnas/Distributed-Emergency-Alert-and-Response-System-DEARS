from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Alert, UserProfile


class UserRegistrationForm(UserCreationForm):
    """Form for new user registration."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address',
        })
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First name',
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last name',
        })
    )
    
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Phone number',
        })
    )
    
    address = forms.CharField(
        max_length=500,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Home address',
        })
    )
    
    city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'City',
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Choose a username',
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Update the user's profile with additional information
            profile = user.profile
            profile.phone_number = self.cleaned_data['phone_number']
            profile.address = self.cleaned_data['address']
            profile.city = self.cleaned_data['city']
            profile.save()
        
        return user


class AlertForm(forms.ModelForm):
    """Form for citizens to submit emergency alerts."""
    
    class Meta:
        model = Alert
        fields = ['emergency_type', 'location', 'latitude', 'longitude', 'description']
        widgets = {
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
            'emergency_type': 'Emergency Type',
            'location': 'Location Description',
            'latitude': 'Latitude (Optional)',
            'longitude': 'Longitude (Optional)',
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
