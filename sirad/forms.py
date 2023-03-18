from django.forms import ModelForm
from .models import Hewan

class SignupForm(ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'