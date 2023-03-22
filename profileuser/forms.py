import uuid
from django import forms
from .models import Customer, Hewan
from ..update_profile.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class FormPendaftaranHewan(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"