import uuid
from django import forms
from .models import Adopsi

class AdopsiForm(forms.ModelForm):
    class Meta:
        model = Adopsi
        fields = "__all__"