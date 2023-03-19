from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Profile
from .forms import UpdateProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.conf import settings
from .forms import UpdateProfile
from .models import Profile, Hewan

@login_required()  
def update_profile(request, id):
    response = {}
    user = get_user(request)
    
    profile = get_object_or_404(Profile, id=id)
    if request.POST:
        form = UpdateProfile(request.POST or None, instance=profile)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.save()
            profile = temp
            return HttpResponseRedirect('/')

    form = UpdateProfile(
            initial={
                "Nama Lengkap": profile.name,
                "Nomor Telepon": profile.number,
                "E-mail": profile.email,
            }
        )
    response['form'] = form
    response['name'] = profile.name
    response['number'] = profile.number
    response['email'] = profile.email

    return render(request, 'update_profile.html', response)