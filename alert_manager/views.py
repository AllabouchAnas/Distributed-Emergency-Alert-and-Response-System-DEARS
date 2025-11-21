# alert_manager/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
from django.urls import reverse

# Khassek t'importer l-Model Alert li ghadi ydirou l-DB Engineer f models.py
# N'supposaw l-model dghya hna bch l-code ykhdem
class Alert:
    # Khasna l-choices dial l-Emergency Type
    class EmergencyType:
        POLICE = 'police'
        FIRE = 'fire'
        MEDICAL = 'medical'
        choices = [
            (POLICE, 'Police Emergency'),
            (FIRE, 'Fire Emergency'),
            (MEDICAL, 'Medical Emergency'),
        ]
        
    @staticmethod
    def get_type_label(type_key):
        for key, label in Alert.EmergencyType.choices:
            if key == type_key:
                return label
        return "Unknown Emergency"

# Hada ghir bch n'simulatew l-Formulaire (machi l-ModelForm)
from django import forms
class DetailsForm(forms.Form):
    full_name = forms.CharField(max_length=100, label="Full Name *", widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    phone_number = forms.CharField(max_length=20, label="Phone Number *", widget=forms.TextInput(attrs={'placeholder': 'Your phone number'}))
    # Coordinates (n'utilisiw des valeurs par défaut kima f l-photo)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6, label="Latitude *", initial=40.7128)
    longitude = forms.DecimalField(max_digits=9, decimal_places=6, label="Longitude *", initial=-74.0060)
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Describe the emergency situation in detail...', 'rows': 4}), label="Description *")


# L-View dial Étape 1: Sélection du type d'urgence
def select_emergency_type(request):
    """Affiche la première page pour sélectionner le type d'urgence."""
    # Les choix sont définis dans le 'context' pour être affichés dans le template
    context = {
        'emergency_types': Alert.EmergencyType.choices
    }
    return render(request, 'alert_manager/step1_select_type.html', context)


# L-View dial Étape 2: Formulaire des détails de l'alerte
@require_http_methods(["GET", "POST"])
def report_details_view(request, alert_type):
    """Affiche le formulaire de détails après la sélection du type d'urgence."""
    
    # T'akéd bli l-type d'urgence sse77
    valid_types = [t[0] for t in Alert.EmergencyType.choices]
    if alert_type not in valid_types:
        return HttpResponseBadRequest("Type d'urgence non valide.")
    
    # Affiche l-Name dial l-type (e.g., 'Police Emergency')
    type_label = Alert.get_type_label(alert_type)

    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            # Hna ghadi tzid l-Logic dial l-REST API m3a l-Dispatcher Server
            final_data = {
                'emergency_type': alert_type,
                **form.cleaned_data # Ajout des autres champs
            }
            
            # SIMULATION: 3وض هاد الكود بالـ call réel لـ Dispatcher RPC
            print(f"ALERTE FINALE ENVOYÉE AU DISPATCHER: {final_data}")
            
            # Kandsiftou l-l-Confirmation Page
            return render(request, 'alert_manager/confirmation.html', {'alert_type': type_label})

    else:
        # GET request: Kan3tih l-form l-khawya
        form = DetailsForm()
        
    context = {
        'form': form,
        'alert_type': alert_type,
        'type_label': type_label,
    }
    return render(request, 'alert_manager/step2_report_details.html', context)