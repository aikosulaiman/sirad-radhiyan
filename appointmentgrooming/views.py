import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from user.models import Customer, User, Hewan, Produk
from .models import AppointmentGrooming
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import IntegrityError, connection

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_appointmentgrooming(request):
    return HttpResponseRedirect("/login")


def list_appointmentgrooming(request):
    response = {}
    return render(request, 'list_appointmentgrooming.html', response)

def read_appointmentgrooming(request, apptgrooming_id):
    cursor = connection.cursor()
    response = {}
    
    if is_authenticated(request):
            if request.method != "POST":
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")
                if len(request.session.keys()) == 0:
                        return redirect('/')
 
                # Fetch object Appointment Grooming
                cursor.execute("""
                SET SEARCH_PATH TO PUBLIC;
                SELECT * 
                FROM appointmentgrooming_appointmentgrooming  
                WHERE ID= '{0}';
                """.format(apptgrooming_id))
                apptgrooming = cursor.fetchall()

                response['apptgrooming'] = apptgrooming

                # Fetch object Customer/Pemilik Hewan/Pendaftar Appointment
                customer_id = apptgrooming[0][7]
                customer = Customer.objects.get(id=customer_id)

                response['customer'] = customer
                    
                customer_login = Customer
                if request.session['Role'] == 'Customer':
                    # Fetch object Customer login
                    uname = request.session['Username']
                    user = User.objects.get(username=uname)
                    customer_login = Customer.objects.get(user_ptr=user)

                if customer_login.id == customer_id or request.session['Role'] == 'Groomer': 
                    

                    # Fetch object Hewan
                    hewan_id = apptgrooming[0][5]
                    hewan = Hewan.objects.get(hewan_id=hewan_id)

                    response['hewan'] = hewan

                    # Fetch object Paket Grooming
                    paket_id = apptgrooming[0][6]
                    paket = Produk.objects.get(id=paket_id)

                    response['paket'] = paket

                    # Fetch object Layanan Tambahan
                    cursor.execute("""
                    SET SEARCH_PATH TO PUBLIC;
                    SELECT * 
                    FROM appointmentgrooming_appointmentgrooming_layanan_tambahan 
                    WHERE appointmentgrooming_id = '{0}';
                    """.format(apptgrooming_id))
                    relasi_tambahan = cursor.fetchall()

                    tambahan = []
                    for i in relasi_tambahan:
                        tambahan_id = i[2]
                        produk = Produk.objects.get(id=tambahan_id)
                        tambahan.append(produk)

                    response['tambahan'] = tambahan                

                    cursor.close()

                    
                    
                    # Fetch data role user yang sedang login
                    role = request.session['Role']
                    response['role'] = role

                    return render(request, 'read_appointmentgrooming.html', response)
                else:
                    context = {
                    'error_message': 'Akses Ditolak!'}
                return render(request, 'error_page_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")
  
def approve_appointmentgrooming(request, apptgrooming_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Groomer':

            status = "Disetujui"
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE appointmentgrooming_appointmentgrooming
                SET status = '{0}'
                WHERE id = '{1}';
                """.format(status, apptgrooming_id)) 
            
        
            success_message = 'Berhasil menyetujui Appointment Grooming!'
            cursor.close()
            return render(request, 'success_page_grooming.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")

def disapprove_appointmentgrooming(request, apptgrooming_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Groomer':

            status = "Ditolak"
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE appointmentgrooming_appointmentgrooming
                SET status = '{0}'
                WHERE id = '{1}';
                """.format(status, apptgrooming_id)) 
            
        
            success_message = 'Berhasil menolak Appointment Grooming!'
            cursor.close()
            return render(request, 'success_page_grooming.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def delete_appointmentgrooming(request, apptgrooming_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            apptgrooming = AppointmentGrooming.objects.get(id=apptgrooming_id)
            
            if apptgrooming.status == "Menunggu Konfirmasi":
                apptgrooming.delete()
                success_message = 'Berhasil membatalkan Appointment Grooming!'
                return render(request, 'success_page_grooming.html', {'success_message': success_message})
            else:
                context = {
                    'error_message': 'Tidak bisa membatalkan Appointment Grooming yang telah disetujui/ditolak.'}
                return render(request, 'error_page_grooming.html', context)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")
