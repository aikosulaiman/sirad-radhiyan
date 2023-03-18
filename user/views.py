from django.shortcuts import get_object_or_404, render
from .models import User
from .forms import UserForm
from django.http import HttpResponseRedirect
from django.db import IntegrityError, connection

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

def update_user(request, user_id):
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
    return render(request, 'user_update.html', response)

def update_user_handler(request, user_id):
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
        return render(request, 'user_update.html', response)

        
    cursor.close()
    return HttpResponseRedirect('/list-user')

