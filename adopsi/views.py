from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import AdopsiForm
from .models import Adopsi
from django.conf import settings
from django.db import IntegrityError, connection
from django.db import connection

# Create your views here.
def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_adopsi(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            form = AdopsiForm()
            if request.method == 'POST':
                form = AdopsiForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    success_message = 'hewan adopsi berhasil ditambah!'
                    return render(request, 'adopt_success.html', {'success_message': success_message})

            return render(request, 'create_adopsi.html', {'form': form})
        else:
            context = {
            'error_message': 'Akses ditolak!'}
            return render(request, 'adopt_error.html', context)
    else:
        return HttpResponseRedirect("/adopsi")

def list_hewan_adopsi(request):
    all_hewan = Adopsi.objects.all().values

    context = {
        'all_hewan': all_hewan,
    }

    return render(request, 'list_hewan_adopsi.html', context)

def read_adopsi(request, hewan_id):
        cursor = connection.cursor()
        
        if request.method != "POST":
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                if len(request.session.keys()) == 0:
                        return redirect('/')
                
                # Fetch object Adopsi
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM adopsi_adopsi  
                WHERE hewan_id= '{0}';
                """.format(hewan_id))
                adopsi = cursor.fetchall()
    
                response = {'adopsi': adopsi, 
                            'hewan_id': hewan_id}
                cursor.close()
                return render(request, 'read_adopsi.html', response)


    

def update_adopsi(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM adopsi_adopsi
    WHERE hewan_id = '{0}' ;
    """.format(user_id))
    user = cursor.fetchall()
        
    response = {
            'user_id':user_id,
            'user':user,}
    cursor.close()
    return render(request, 'update_adopsi.html', response)

def update_adopsi_handler(request, user_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # get data dari form
    nama = request.GET.get('nama')
    jenis = request.GET.get('jenis')
    ras = request.GET.get('ras')
    warna = request.GET.get('warna')
    deskripsi = request.GET.get('deskripsi')

    try:
        # update
       cursor.execute("""
       UPDATE adopsi_adopsi
       SET nama = '{0}', jenis = '{1}', ras = '{2}', warna = '{3}', deskripsi = '{4}'
       WHERE hewan_id = '{5}';
       """.format(nama, jenis, ras, warna, deskripsi, user_id))
       success_message = 'Hewan berhasil diupdate!'
       return render(request, 'adopt_success.html', {'success_message': success_message})
    except IntegrityError:
        # If the field is not unique, return an error message
        error_message = 'There was and error.'
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
        return render(request, 'update_adopsi.html', response)

        
    cursor.close()
    return HttpResponseRedirect('/adopsi')