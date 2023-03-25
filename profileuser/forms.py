from django import forms
from .models import User, VipValidation

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class VipValidationForm(forms.ModelForm):
    class Meta:
        model = VipValidation
        fields = "__all__"