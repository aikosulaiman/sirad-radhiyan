from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import get_user, login, logout
from loginlogout.forms import *
from django.contrib.auth.views import LoginView


# Create your views here.
def index(request):
    return render(request, 'index.html')

