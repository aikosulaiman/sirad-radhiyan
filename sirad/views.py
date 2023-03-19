from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    return render(request, 'base.html')

def read_profile(request):
    return render(request, 'read-profile.html')