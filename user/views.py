from django.shortcuts import render
from .models import User
from .forms import UserForm
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'base.html')

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def add_user(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            form = UserForm()
            if request.method == 'POST':
                form = UserForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/user/list-user')
                else:
                    form.add_error(None, "Username already exists")
            response = {'form': form}
            return render(request, 'user_add.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")


def list_user(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            user_admin = User.objects.filter(role="Admin") #Filter Role Admin
            user_customer = User.objects.filter(role="Customer") #Filter Role Customer
            user_dokter = User.objects.filter(role="Dokter") #Filter Role Dokter
            user_groomer = User.objects.filter(role="Groomer") #Filter Role Groomer
            user_karyawan = User.objects.filter(role="Karyawan") #Filter Role Karyawan
            
            user = User.objects.all().values()

            response = {'user':user,
                        'user_admin':user_admin,
                        'user_customer':user_customer,
                        'user_dokter':user_dokter,
                        'user_groomer':user_groomer,
                        'user_karyawan':user_karyawan
                        }
            return render(request, 'user_list.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def delete_user(request, id):
    user_by_id = User.objects.get(id=id)
    user_by_id.delete()
    return HttpResponseRedirect('/user/list-user')