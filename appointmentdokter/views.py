from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from .forms import AppointmentDokterForm

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_appointmentdokter(request):
    if request.method == 'POST':
        form = AppointmentDokterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = AppointmentDokterForm()
    return render(request, 'create_appointmentdokter.html', {'form': form})
