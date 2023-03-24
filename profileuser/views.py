from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
# from ..profileuser.forms import UserForm
from .models import User, Hewan
from django.db import IntegrityError, connection

def index(request):
    return HttpResponseRedirect("/")

def read_profile(request, username):
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
    cursor.close()
    print(user)
    return render(request, 'read_profile.html', response)

def vip_form(request):
    return render(request, 'vip_form.html')

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

# @login_required()  
# def update_profile(request, id):
#     response = {}
#     user = get_user(request)
    
#     profile = get_object_or_404(User, id=id)
#     if request.POST:
#         form = UserForm(request.POST or None, instance=profile)
#         if form.is_valid():
#             temp = form.save(commit=False)
#             temp.save()
#             profile = temp
#             return HttpResponseRedirect('/')

#     form = UserForm(
#             initial={
#                 "Nama Depan": profile.first_name,
#                 "Nama Belakang": profile.last_name,
#                 "Nomor Telepon": profile.no_telepon,
#                 "E-mail": profile.email,
#             }
#         )
#     response['form'] = form
#     response['first_name'] = profile.first_name
#     response['last_name'] = profile.last_name
#     response['no_telepon'] = profile.no_telepon
#     response['email'] = profile.email

#     return render(request, 'update_profile.html', response)