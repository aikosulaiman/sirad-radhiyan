from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
# from ..profileuser.forms import UserForm
from .models import User
from django.db import IntegrityError, connection

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