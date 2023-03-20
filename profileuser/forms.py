import uuid
from django import forms
from .models import Customer, Hewan

class CustomerForm(forms.ModelForm):
    is_vip = forms.BooleanField(default=False)

class FormPendaftaranHewan(forms.Form):
    hewan_id = forms.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = forms.CharField(max_length = 50)
    jenis = forms.CharField(max_length = 50)
    umur = forms.CharField(max_length = 50)
    note = forms.CharField(max_length = 50)