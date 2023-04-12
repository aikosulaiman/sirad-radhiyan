from django import forms
from .models import AppointmentDokter

class AppointmentDokterForm(forms.ModelForm):
    class Meta:
        model = AppointmentDokter
        fields = ('dokter', 'hewan', 'appointment_date')
        labels = {
            'dokter': 'Dokter',
            'hewan': 'Hewan',
            'appointment_date': 'Appointment Date and Time'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dokter'].empty_label = 'Select a doctor'
        self.fields['hewan'].empty_label = 'Select a patient'
        self.fields['appointment_date'].widget.attrs['autocomplete'] = 'off'
