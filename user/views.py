import uuid
from django.shortcuts import render
from .models import User, Produk, Customer
from appointmentgrooming.models import AppointmentGrooming
from .forms import UserForm, CustomerForm, ProdukForm
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError, connection

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
                    form.add_error(None, "Username or email already exists, please choose another one!")
            response = {'form': form,
                        'username':request.session['Username']}
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
                        'user_karyawan':user_karyawan,
                        'username':request.session['Username']
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

def update_user(request, user_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
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
                    'user':user,
                    'username':request.session['Username']}
            cursor.close()
            return render(request, 'user_update.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def update_user_handler(request, user_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            # get data dari form
            username = request.GET.get('username')
            first_name = request.GET.get('first_name')
            last_name = request.GET.get('last_name')
            email = request.GET.get('email')
            no_telepon = request.GET.get('no_telepon')

            try:
                # update
                cursor.execute("""
                UPDATE user_user
                SET username = '{0}', first_name = '{1}', last_name = '{2}', email = '{3}', no_telepon = '{4}'
                WHERE id = '{5}';
                """.format(username, first_name, last_name, email, no_telepon, user_id))
                success_message = 'User updated successfully!'
                cursor.close()
                return render(request, 'success_page_user.html', {'success_message': success_message})
            except IntegrityError:
                # If the field is not unique, return an error message
                error_message = 'Username or Email is already taken. Please choose another one.'
                cursor.execute("""
                SELECT *
                FROM user_user
                WHERE id = '{0}' ;
                """.format(user_id))
                user = cursor.fetchall()
                response = {
                    'error_message': error_message,
                    'user':user,
                    'user_id': user_id,
                    'username':request.session['Username']}
                cursor.close()
                return render(request, 'user_update.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_customer(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Karyawan':
            
            customer = Customer.objects.all().values()

            response = {
                        'customer':customer,
                        'username':request.session['Username']
                        }
            return render(request, 'customer_list.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def customer_approval(request, id):
    customer_by_id = Customer.objects.get(id=id)
    customer_by_id.is_vip = True
    customer_by_id.save()
    return HttpResponseRedirect('/user/list-customer')


def customer_registration(request):
    form = CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        else:
            form.add_error(None, "Username or email already exists, please choose another one!")
    response = {'form': form,}
    return render(request, 'customer_registration.html', response)

def list_produk(request):
    cursor = connection.cursor()
    response = {}

    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")
            layanan = Produk.objects.filter(jenis="Layanan")
            produk = Produk.objects.filter(jenis="Produk") 
            
            # Fetch all id paket (produk)
            cursor.execute("""
            SET SEARCH_PATH TO PUBLIC;
            SELECT paket_id 
            FROM appointmentgrooming_appointmentgrooming;
            """)
            paket_id = cursor.fetchall()
            paket_id_all = [x[0] for x in paket_id]

            # Fetch all id layanan tambahan (layanan)
            cursor.execute("""
            SET SEARCH_PATH TO PUBLIC;
            SELECT produk_id 
            FROM appointmentgrooming_appointmentgrooming_layanan_tambahan;
            """)
            layanan_id = cursor.fetchall()
            layanan_id_all = [x[0] for x in layanan_id]
    
            cursor.close()

            
            response = {'layanan':layanan, 'produk':produk, 'paket_id_all':paket_id_all, 'layanan_id_all':layanan_id_all, 'username':request.session['Username']}
            return render(request, 'produk_list.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def add_produk(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            form = ProdukForm()
            if request.method == 'POST':
                form = ProdukForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/user/list-produk')
                else:
                    form.add_error(None, "Nama produk sudah ada, silakan memilih nama lain!")
            response = {'form': form}
            return render(request, 'produk_add.html', response)
        else:
            context = {
            'error_message': 'Access denied!', 'username':request.session['Username']}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def delete_produk(request, id):
    produk_by_id = Produk.objects.get(id=id)
    produk_by_id.delete()
    return HttpResponseRedirect('/user/list-produk')

def update_produk(request, produk_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            # Mencari produk
            cursor.execute("""
            SELECT *
            FROM user_produk
            WHERE id = '{0}' ;
            """.format(produk_id))
            produk = cursor.fetchall()
                
            status = produk[0][3]

            response = {
                    'produk_id':produk_id,
                    'produk':produk,
                    'status':status,
                    'username':request.session['Username']}
            cursor.close()
            return render(request, 'produk_update.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")

def update_produk_handler(request, produk_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Admin':
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            # get data dari form
            nama = request.GET.get('nama')
            harga = request.GET.get('harga')
            status = request.GET.get('status')

            try:
                # update
                cursor.execute("""
                UPDATE user_produk
                SET nama = '{0}', harga = '{1}', status = '{2}'
                WHERE id = '{3}';
                """.format(nama, harga, status, produk_id))
                success_message = 'Produk berhasil diupdate!'
                cursor.close()
                return render(request, 'success_page_produk.html', {'success_message': success_message})
            except IntegrityError:
                # If the field is not unique, return an error message
                error_message = 'Nama produk sudah ada, silakan memilih nama lain!'
                cursor.execute("""
                SELECT *
                FROM user_produk
                WHERE id = '{0}' ;
                """.format(produk_id))
                produk = cursor.fetchall()
                response = {
                    'error_message': error_message,
                    'produk':produk,
                    'produk_id': produk_id,
                    'username':request.session['Username']}
                cursor.close()
                return render(request, 'produk_update.html', response)
        else:
            context = {
            'error_message': 'Access denied!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
