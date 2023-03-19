from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import UpdateProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from django.conf import settings
from .forms import UpdateProfile
from .models import User

@login_required()  
def update_profile(request, id):
    response = {}
    user = get_user(request)
    
    profile = get_object_or_404(User, id=id)
    if request.POST:
        form = UpdateProfile(request.POST or None, instance=profile)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.save()
            profile = temp
            return HttpResponseRedirect('/')

    form = UpdateProfile(
            initial={
                "Nama Depan": profile.first_name,
                "Nama Belakang": profile.last_name,
                "Nomor Telepon": profile.no_telepon,
                "E-mail": profile.email,
            }
        )
    response['form'] = form
    response['first_name'] = profile.first_name
    response['last_name'] = profile.last_name
    response['no_telepon'] = profile.no_telepon
    response['email'] = profile.email

    return render(request, 'update_profile.html', response)