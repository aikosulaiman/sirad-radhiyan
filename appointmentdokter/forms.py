from django import forms
from .models import AppointmentDokter, Dokter, Hewan
from django.utils import timezone
from django.db.models import Q

class DokterModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.first_name} ({obj.last_name})"

class HewanModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama}"

class AppointmentDokterForm(forms.ModelForm):
    dokter = DokterModelChoiceField(queryset=Dokter.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    hewan = HewanModelChoiceField(queryset=Hewan.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = AppointmentDokter
    
        fields = ('dokter', 'hewan', 'appointment_time', 'keluhan')
        # labels = {
        #     'dokter': 'Dokter',
        #     'hewan': 'Hewan',
        #     'appointment_time': 'Appointment Date and Time',
        #     'keluhan': 'Keluhan'
        # }
        widgets = {
            'appointment_time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['dokter'].empty_label = 'Pilih dokter hewan'
    #     self.fields['hewan'].empty_label = 'Pilih hewan peliharaan'
    #     self.fields['keluhan'].empty_label = 'Masukkan keluhan hewan peliharaaanmu'


    # def clean(self):
    #     cleaned_data = super().clean()
    #     appointment_time = cleaned_data.get('appointment_time')
    #     if appointment_time < timezone.now():
    #         raise forms.ValidationError('Appointment cannot be in the past')