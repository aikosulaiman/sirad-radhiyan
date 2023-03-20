import uuid
from django import forms
from .models import Customer, Hewan

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
    # id = forms.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # username = forms.CharField(max_length = 50)
    # first_name = forms.CharField(max_length = 50)
    # last_name = forms.CharField(max_length = 50)
    # email = forms.CharField(max_length = 50)
    # no_telepon = forms.CharField(max_length = 50)
    # password = forms.CharField(max_length = 50)

class FormPendaftaranHewan(forms.Form):
    class Meta:
        model = Hewan
        fields = '__all__'
    # hewan_id = forms.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # nama = forms.CharField(max_length = 50)
    # jenis = forms.CharField(max_length = 50)
    # umur = forms.CharField(max_length = 50)
    # note = forms.CharField(max_length = 50)