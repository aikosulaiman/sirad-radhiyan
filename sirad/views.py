from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'base.html')

def customer_registration(request):
    return render(request, 'customer-registration.html')

def read_profile(request):
    return render(request, 'read-profile.html')
