import uuid
from django import forms
from .models import Customer, Hewan

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class FormPendaftaranHewan(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'