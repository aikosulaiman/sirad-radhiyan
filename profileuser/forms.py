from django import forms
from ..update_profile.models import User, Customer, Hewan


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

class FormPendaftaranHewan(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'