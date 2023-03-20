from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Hewan
from .forms import FormPendaftaranHewan, CustomerForm

def index(request):
    return render(request, 'base.html')
