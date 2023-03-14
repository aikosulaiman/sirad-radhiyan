from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from .forms import LoginForm
from django.db import connection

def home(request):
    return render(request, 'index.html', context=dict(request.session))

def login(request) :
    cursor = connection.cursor()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            cursor.execute("SET search_path TO public")
            cursor.execute('SELECT * FROM public."User" WHERE "User"."Username"=%s AND "User"."Password"=%s', [username, password])
            user = cursor.fetchall()
            print(user)
            if len(user) > 0:
                request.session["Username"] = user[0][1]
                request.session["Email"] = user[0][2]
                request.session["Role"] = user[0][6]
                return redirect('/')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    request.session.clear()
    return HttpResponseRedirect("/login")