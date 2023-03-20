from django import forms
from .models import Profile, Hewan

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'number', 'email']
    
    def save(self, commit=True):
        profile = self.instance
        profile.name = self.cleaned_data['name']
        profile.number = self.cleaned_data['number']
        profile.email = self.cleaned_data['email']

        if commit:
            profile.save()
        return profile
