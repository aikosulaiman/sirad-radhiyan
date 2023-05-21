from django import forms
from .models import AppointmentGrooming, Hewan, Produk
from django.utils import timezone
from django.db.models import Q

class HewanModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama}"

class PaketModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama} ({obj.harga})"
    
class LayananTambahanModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nama} ({obj.harga})"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-list'})



class AppointmentGroomingForm(forms.ModelForm):
    hewan = HewanModelChoiceField(queryset=Hewan.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    
    paket = PaketModelChoiceField(queryset=Produk.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    
    layanan_tambahan = forms.ModelMultipleChoiceField(
        queryset=Produk.objects.all(),
        required=False
    )
    
    class Meta:
        model = AppointmentGrooming
    
        fields = ( 'hewan', 'appointment_time', 'paket', 'layanan_tambahan')
        widgets = {
            'appointment_time': forms.TextInput(attrs={'type': 'datetime-local'}),
        }
