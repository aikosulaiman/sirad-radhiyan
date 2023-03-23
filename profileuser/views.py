import uuid
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
# from ..profileuser.forms import UserForm
from .models import User, Customer, Hewan
from django.db import IntegrityError, connection
from .forms import FormPendaftaranHewan

def index(request):
    return HttpResponseRedirect("/")

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
        error_message = 'Username or email is already taken. Please choose another one.'
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
    return HttpResponseRedirect('/profile')

def form_pendaftaran_hewan(request) :
    cursor = connection.cursor()
    if request.method == 'POST':
        form = FormPendaftaranHewan(request.POST)
        if form.is_valid():
            hewan_id = uuid.uuid4()
            nama = form.cleaned_data['nama']
            jenis = form.cleaned_data['jenis']
            umur = form.cleaned_data['umur']
            note = form.cleaned_data['note']
            cursor.execute("SET search_path TO public")
            cursor.execute('INSERT INTO profileuser_hewan VALUES (%s, %s, %s, %s, %s)', [hewan_id, nama, jenis, umur, note])
            return redirect('/profile')
    else:
        form = FormPendaftaranHewan()
    return render(request, 'form_pendaftaran_hewan.html', {'form': form})

# def delete_hewan(request, id):
#     hewan_by_id = Hewan.objects.get(id=id)
#     hewan_by_id.delete()
#     return HttpResponseRedirect('/profile')

def payment_form(request):
    context = {}
    return render(request, 'payment_form.html', context)

def update_hewan(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM user_hewan
    WHERE hewan_id = '{0}' ;
    """.format(user_id))
    user = cursor.fetchall()
        
    response = {
            'user_id':user_id,
            'user':user,}
    cursor.close()
    return render(request, 'update_hewan.html', response)

def update_hewan_handler(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # get data dari form
    nama = request.GET.get('nama')
    jenis = request.GET.get('jenis')
    umur = request.GET.get('umur')
    note = request.GET.get('note')

    try:
        # update
        cursor.execute("""
        UPDATE user_hewan
        SET nama = '{0}', jenis = '{1}', umur = '{2}', note = '{3}'
        WHERE hewan_id = '{4}';
        """.format(nama, jenis, umur, note, user_id))
        success_message = 'Hewan updated successfully!'
        return render(request, 'update_success.html', {'success_message': success_message})
    except IntegrityError:
        # If the field is not unique, return an error message
        error_message = 'Username or email is already taken. Please choose another one.'
        cursor.execute("""
        SELECT *
        FROM user_hewan
        WHERE hewan_id = '{0}' ;
        """.format(user_id))
        user = cursor.fetchall()
        response = {
            'error_message': error_message,
            'user':user,
            'user_id': user_id}
        return render(request, 'update_hewan.html', response)

        
    cursor.close()
    return HttpResponseRedirect('/profile')
