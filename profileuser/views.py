from django.http.response import HttpResponseRedirect
from django.conf import settings
from django.db import IntegrityError, connection
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
import io
from PIL import Image
from supabase.client import Client

SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY

def index(request):
    return HttpResponseRedirect("/")

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def read_profile(request, username):
    if is_authenticated(request):
        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

        # Mencari user
        cursor.execute("""
        SELECT *
        FROM user_user
        WHERE username = '{0}' ;
        """.format(username))
        user = cursor.fetchall()
            
        response = {
                'user_id':user[0][0],
                'username':username,
                'user_first_name':user[0][2],
                'user_last_name':user[0][3],
                'user_role':user[0][4],
                'user_email':user[0][5],
                'user_no_telepon':user[0][6],
                'user':user}

        if response['user_role'] == 'Customer':
            cursor.execute("""
            SELECT *
            FROM user_customer
            WHERE user_ptr_id = '{0}' ;
            """.format(response['user_id']))
            user = cursor.fetchall()

            response['user_is_vip'] = user[0][1]

            cursor.execute("""
            SELECT *
            FROM user_hewan
            WHERE pemilik_id = '{0}' ;
            """.format(response['user_id']))
            list_hewan = cursor.fetchall()
            print(list_hewan)

            response['list_hewan'] = list_hewan

            cursor.close()
            return render(request, 'read_profile_customer.html', response)
        elif response['user_role'] == 'Dokter':
            cursor.execute("""
            SELECT *
            FROM user_dokter
            WHERE user_ptr_id = '{0}' ;
            """.format(response['user_id']))
            user = cursor.fetchall()

            response['user_tarif'] = user[0][1]
            cursor.close()
            return render(request, 'read_profile_dokter.html', response)
        else:
            cursor.close()
            return render(request, 'read_profile.html', response)
    else:
        return HttpResponseRedirect("/login")

def submit_vip_validation(request, user_id):
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
    return render(request, 'submit_vip_validation.html', response)

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

# def tambah_hewan(request, user_id):
#     form = HewanForm()
#     if request.method == 'POST':
#         form = HewanForm(request.POST or None)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/')
#         else:
#             print(form.errors)
#             # form.add_error(None, "Username or email already exists, please choose another one!")
#     response = {
#         'form': form,
#         'user_id':user_id
#         }
#     return render(request, 'tambah_hewan.html', response)

def tambah_hewan(request, user_id):
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
    return render(request, 'tambah_hewan.html', response)

def tambah_hewan_handler(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # get data dari form
    nama = request.POST.get('nama')
    jenis = request.POST.get('jenis')
    umur = request.POST.get('umur')
    note = request.POST.get('note')

    try:
        # update
        cursor.execute('''
        INSERT INTO user_hewan (nama, jenis, umur, note, pemilik_id)
        VALUES (%s, %s, %s, %s, %s);
        ''', (nama, jenis, umur, note, user_id))
        success_message = 'Hewan Anda berhasil didaftarkan!'
        return render(request, 'tambah_hewan_success.html', {'success_message': success_message})
    except IntegrityError as e:
        # If the field is not unique, return an error message
        error_message = 'Hewan Anda gagal ditambahkan.'
        cursor.execute("""
        SELECT *
        FROM user_user
        WHERE id = '{0}' ;
        """.format(user_id))
        user = cursor.fetchall()
        response = {
            'error_message': e.__cause__,
            'user':user,
            'user_id': user_id}
        return render(request, 'tambah_hewan.html', response)

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

def delete_hewan(request, hewan_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    DELETE
    FROM user_hewan
    WHERE hewan_id = '{0}' ;
    """.format(hewan_id))
    cursor.close()
    success_message = 'Hewan ini berhasil dihapus!'
    return render(request, 'delete_success.html', {'success_message': success_message})