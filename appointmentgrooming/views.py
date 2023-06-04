import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from appointmentgrooming.forms import AppointmentGroomingForm
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast
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
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            my_username = request.session['Username']
            my_uuid = str(request.session['UUID'])
            list_hewan = Hewan.objects.filter(pemilik_id=my_uuid)
            list_paket = Produk.objects.filter(jenis="Produk")
            list_tambahan = Produk.objects.filter(jenis="Layanan")
            

            if request.method == 'POST':
                form = AppointmentGroomingForm(request.POST)
                print(form.errors)
                if form.is_valid():
                    appointment = form.save(commit=False)
                    
                    hewan = form.cleaned_data['hewan']
                    if hewan:
                        appointment.hewan = hewan

                    cust_instance = Customer.objects.get(username=request.session["Username"])
                    appointment.pemilik = cust_instance
                    appointment.status = 'Menunggu Konfirmasi'
                    
                    appointment.total_biaya = 0

                    # Get the selected layanan_tambahan checkboxes
                    selected_layanan_tambahan = request.POST.getlist('layanan_tambahan', [])

                    # Save the appointment object
                    appointment.save()

                    # Add the selected layanan_tambahan to the appointment
                    if selected_layanan_tambahan:
                        appointment.layanan_tambahan.set(selected_layanan_tambahan)

                    # Calculate the total_biaya
                    appointment.total_biaya = int(appointment.paket.harga)
                    
                    layanan_tambahan_harga = appointment.layanan_tambahan.annotate(harga_numeric=Cast('harga', IntegerField())).aggregate(total=Sum('harga_numeric'))['total']
                    if layanan_tambahan_harga is None:
                        layanan_tambahan_harga = 0  
                    appointment.total_biaya += int(layanan_tambahan_harga)
                    appointment.save()
                    

                    success_message = 'Appointment Grooming dengan ID ' + appointment.appointment_id + ' berhasil terbuat!'
                    context = {'success_message': success_message,
                               'apptgrooming_id': appointment.id,
                               'apptgrm_id': appointment.appointment_id}
                    return render(request, 'success_page_grooming.html', context)
                else:
                    print("FORM ERROR:\n")
                    print(form.errors)
                    print("\nItu errornya di atas")
            else:
                form = AppointmentGroomingForm()
                
            context = {
                'listHewan': list_hewan,
                'list_paket': list_paket,
                'list_tambahan': list_tambahan,
                'form': form,
                'user_id': my_uuid,
                'username': my_username,
            }
            return render(request, 'create_appointmentgrooming.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_appointmentgrooming(request):
    if is_authenticated(request):
        my_username = request.session['Username']
        my_uuid = str(request.session['UUID'])
        list_appointmentgrooming = []
        list_disetujui = []
        list_konfirmasi = []
        list_ditolak = []
        list_dibatalkan = []
        list_selesai = []
        if request.session['Role'] == 'Customer':
            list_appointmentgrooming = AppointmentGrooming.objects.filter(pemilik_id=my_uuid).order_by('-id')

            list_disetujui = AppointmentGrooming.objects.filter(pemilik_id=my_uuid, status='Disetujui').order_by('-id')

            list_konfirmasi = AppointmentGrooming.objects.filter(pemilik_id=my_uuid, status='Menunggu Konfirmasi').order_by('-id')

            list_ditolak = AppointmentGrooming.objects.filter(pemilik_id=my_uuid, status='Ditolak').order_by('-id')

            list_dibatalkan = AppointmentGrooming.objects.filter(pemilik_id=my_uuid, status='Dibatalkan').order_by('-id')

            list_selesai = AppointmentGrooming.objects.filter(pemilik_id=my_uuid, status='Selesai').order_by('-id')

        elif request.session['Role'] == 'Groomer' or request.session['Role'] == 'Admin':
            list_appointmentgrooming = AppointmentGrooming.objects.all().order_by('-id')

            list_disetujui = AppointmentGrooming.objects.filter(status='Disetujui').order_by('-id')

            list_konfirmasi = AppointmentGrooming.objects.filter(status='Menunggu Konfirmasi').order_by('-id')

            list_ditolak = AppointmentGrooming.objects.filter(status='Ditolak').order_by('-id')

            list_dibatalkan = AppointmentGrooming.objects.filter(status='Dibatalkan').order_by('-id')

            list_selesai = AppointmentGrooming.objects.filter(status='Selesai').order_by('-id')

        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_grooming.html', context)
        context = {
            'list_appointmentgrooming': list_appointmentgrooming,
            'list_disetujui': list_disetujui,
            'list_konfirmasi': list_konfirmasi,
            'list_ditolak': list_ditolak,
            'list_dibatalkan': list_dibatalkan,
            'list_selesai': list_selesai,
            'username': my_username,
        }
        return render(request, 'list_appointmentgrooming.html', context)
    else:
        return HttpResponseRedirect("/login")
        
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
            
            appointment = AppointmentGrooming.objects.get(id=apptgrooming_id)
            
        
            success_message = 'Appointment Grooming dengan ID ' + appointment.appointment_id + ' berhasil disetujui!'
            context = {'success_message': success_message,
                        'apptgrooming_id': apptgrooming_id,
                        'apptgrm_id': appointment.appointment_id}
            return render(request, 'success_page_grooming.html', context)
                     
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
            
            appointment = AppointmentGrooming.objects.get(id=apptgrooming_id)
            
            success_message = 'Appointment Grooming dengan ID ' + appointment.appointment_id + ' berhasil ditolak!'
            cursor.close()
            context = {'success_message': success_message,
                        'apptgrooming_id': apptgrooming_id,
                        'apptgrm_id': appointment.appointment_id}
            return render(request, 'success_page_grooming.html', context)
                     
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
                apptgrm_id = apptgrooming.appointment_id
                apptgrooming.delete()
                success_message = 'Appointment Grooming dengan ID ' + apptgrm_id + ' berhasil dibatalkan!'
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

def update_appointmentgrooming(request, apptgrooming_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            # Fetch object Customer login
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer_login = Customer.objects.get(user_ptr=user)

            # Retrieve the updated appointment object
            appointment = AppointmentGrooming.objects.get(id=apptgrooming_id)

            if customer_login == appointment.pemilik:
                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                # Mencari appointmentgrooming
                cursor.execute("""
                SELECT *
                FROM appointmentgrooming_appointmentgrooming
                WHERE id = '{0}' ;
                """.format(apptgrooming_id))
                apptgrooming = cursor.fetchall()

                paket_id = apptgrooming[0][6]
                paket = Produk.objects.get(id=paket_id)

                hewan_id = apptgrooming[0][5]
                hewan = Hewan.objects.get(hewan_id=hewan_id)

                appointment_time = apptgrooming[0][2]

                apptgrm_id = apptgrooming[0][1]

                my_uuid = str(request.session['UUID'])
                list_hewan = Hewan.objects.filter(pemilik_id=my_uuid)
                list_paket = Produk.objects.filter(jenis="Produk")
                list_tambahan = Produk.objects.filter(jenis="Layanan")
                
                appointment_layanan_tambahan = appointment.layanan_tambahan.all()
                
                response = {
                    'apptgrooming_id': apptgrooming_id,
                    'apptgrm_id': apptgrm_id,
                    'paket': paket,
                    'paket_id': paket_id,
                    'hewan': hewan,
                    'hewan_id': hewan_id,
                    'appointment_time': appointment_time,
                    'list_hewan': list_hewan,
                    'list_paket': list_paket,
                    'list_tambahan': list_tambahan,
                    'appointment_layanan_tambahan': appointment_layanan_tambahan
                }
                cursor.close()
                return render(request, 'update_appointmentgrooming.html', response)
            else:
                return render(request, 'error_page.html', {'error_message': 'Akses Ditolak!'})
        else:
            context = {'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")
    

def update_appointmentgrooming_handler(request, apptgrooming_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            # Fetch object Customer login
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer_login = Customer.objects.get(user_ptr=user)

            # Retrieve the updated appointment object
            appointment = AppointmentGrooming.objects.get(id=apptgrooming_id)

            if customer_login == appointment.pemilik:
                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                # get data from form
                paket = request.POST.get('paket')
                hewan = request.POST.get('hewan')
                layanan_tambahan = request.POST.getlist('layanan_tambahan')
                appointment_time = request.POST.get('appointment_time')

                try:
                    # update appointmentgrooming
                    cursor.execute("""
                        UPDATE appointmentgrooming_appointmentgrooming
                        SET paket_id = %s, hewan_id = %s, appointment_time = %s
                        WHERE id = %s;
                    """, [paket, hewan, appointment_time, apptgrooming_id])

                    # update appointmentgrooming_layanan_tambahan
                    cursor.execute("""
                        DELETE FROM appointmentgrooming_appointmentgrooming_layanan_tambahan
                        WHERE appointmentgrooming_id = %s;
                    """, [apptgrooming_id])

                    for tambahan_id in layanan_tambahan:
                        cursor.execute("""
                            INSERT INTO appointmentgrooming_appointmentgrooming_layanan_tambahan (appointmentgrooming_id, produk_id)
                            VALUES (%s, %s);
                        """, [apptgrooming_id, tambahan_id])

                    cursor.close()

                    # Fetch the updated appointment object after the changes
                    appointment = AppointmentGrooming.objects.get(id=apptgrooming_id)

                    # Calculate the total_biaya
                    appointment.total_biaya = int(appointment.paket.harga)
                    
                    layanan_tambahan_harga = appointment.layanan_tambahan.annotate(harga_numeric=Cast('harga', IntegerField())).aggregate(total=Sum('harga_numeric'))['total']
                    if layanan_tambahan_harga is None:
                        layanan_tambahan_harga = 0  
                    appointment.total_biaya += int(layanan_tambahan_harga)
                    appointment.save()


                    success_message = 'Appointment Grooming dengan ID ' + appointment.appointment_id + ' berhasil diubah!'
                    context = {'success_message': success_message,
                               'apptgrooming_id': apptgrooming_id,
                               'apptgrm_id': appointment.appointment_id}
                    return render(request, 'success_page_grooming.html', context)
                except IntegrityError:
                    pass
            else:
                return render(request, 'error_page.html', {'error_message': 'Akses Ditolak!'})
        else:
            context = {'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page.html', context)
    else:
        return HttpResponseRedirect("/login")