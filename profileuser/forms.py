import uuid
from django import forms
<<<<<<< HEAD
from .models import Customer, Hewan, User
=======
from .models import User, VipValidation, Hewan
>>>>>>> 4062d8683f7c4d944e5edae0a2c70ede8f6c4efc

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

<<<<<<< HEAD
class FormPendaftaranHewan(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = '__all__'
=======
class VipValidationForm(forms.ModelForm):
    class Meta:
        model = VipValidation
        fields = "__all__"

class HewanForm(forms.ModelForm):
    class Meta:
        model = Hewan
        fields = "__all__"
>>>>>>> 4062d8683f7c4d944e5edae0a2c70ede8f6c4efc
