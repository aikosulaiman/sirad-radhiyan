import uuid
from django import forms
from .models import User, VipValidation, Hewan

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class VipValidationForm(forms.ModelForm):
    class Meta:
        model = VipValidation
        fields = "__all__"

class HewanForm(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = "__all__"