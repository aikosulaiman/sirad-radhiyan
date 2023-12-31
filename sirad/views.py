from contextlib import nullcontext
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

# Create your views here.
def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False


def index(request):
    print(is_authenticated)
    if is_authenticated(request):
        context = {}
        context['username'] = request.session['Username']
        if request.session['Role'] == 'Admin':
            return render(request, 'home_admin.html', context)
        elif request.session['Role'] == 'Customer':
            return render(request, 'home_customer.html', context)
        elif request.session['Role'] == 'Dokter':
            return render(request, 'home_dokter.html', context)
        elif request.session['Role'] == 'Groomer':
            return render(request, 'home_groomer.html', context)
        elif request.session['Role'] == 'Karyawan':
            return render(request, 'home_karyawan.html', context)
    else:
        return HttpResponseRedirect("/login")
