from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
# from ..profileuser.forms import UserForm
from .models import User, Customer
from django.db import IntegrityError, connection
from .forms import CustomerForm, FormPendaftaranHewan

def index(request):
    return render(request, 'base.html')

def update_profile(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM user_user
    WHERE id = '{0}' ;
    """.format(user_id))
    user = cursor.fetchall()
        
    response = {
            'user_id':user_id,
            'user':user,}
    cursor.close()
    return render(request, 'update_profile.html', response)

def update_profile_handler(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # get data dari form
    username = request.GET.get('username')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    email = request.GET.get('email')
    no_telepon = request.GET.get('no_telepon')
    password = request.GET.get('password')

    try:
        # update
        cursor.execute("""
        UPDATE user_user
        SET username = '{0}', first_name = '{1}', last_name = '{2}', email = '{3}', no_telepon = '{4}', password = '{5}'
        WHERE id = '{6}';
        """.format(username, first_name, last_name, email, no_telepon, password, user_id))
        success_message = 'Profile updated successfully!'
        return render(request, 'update_success.html', {'success_message': success_message})
    except IntegrityError:
        # If the field is not unique, return an error message
        error_message = 'This field is already taken. Please choose another one.'
        cursor.execute("""
        SELECT *
        FROM user_user
        WHERE id = '{0}' ;
        """.format(user_id))
        user = cursor.fetchall()
        response = {
            'error_message': error_message,
            'user':user,
            'user_id': user_id}
        return render(request, 'update_profile.html', response)

        
    cursor.close()
    return HttpResponseRedirect('/list-user')

def customer_registration(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('Index')

    response = {'form': form}
    return render(request, 'customer_registration.html', response)


def form_pendaftaran_hewan(request):
    form = FormPendaftaranHewan()
    if request.method == 'POST':
        form = FormPendaftaranHewan(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Index')

    context = {'form': form}
    return render(request, 'form_pendaftaran_hewan.html', context)

def payment_form(request):
    context = {}
    return render(request, 'payment_form.html', context)