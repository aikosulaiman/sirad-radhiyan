import uuid
from django import forms
from .models import Customer, Hewan, User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class FormPendaftaranHewan(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'