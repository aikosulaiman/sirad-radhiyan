from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hewan
from .forms import SignupForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def customer_registration(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('Index')

    return render(request, 'customer_registration.html', {'form':form})

def index(request):
    return render(request, 'base.html')

def signup_form(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Index')

    context = {'form': form}
    return render(request, 'signup_form.html', context)