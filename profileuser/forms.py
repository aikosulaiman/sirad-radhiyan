from django import forms
from ..update_profile.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"