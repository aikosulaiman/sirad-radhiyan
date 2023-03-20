from django.shortcuts import render
from .models import User
from .forms import UserForm
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'base.html')

def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/list-user')
    response = {'form': form}
    return render(request, 'user_add.html', response)

def list_user(request):
    user = User.objects.all().values()
    response = {'user':user}
    return render(request, 'user_list.html', response)

