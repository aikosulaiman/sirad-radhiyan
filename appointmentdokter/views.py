from sqlite3 import IntegrityError
from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import IntegrityError, connection

from user.models import User, Customer, Dokter, Hewan
from .forms import AppointmentDokterForm
from .models import AppointmentDokter

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def create_appointmentdokter(request):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            my_username = request.session['Username']
            my_uuid = str(request.session['UUID'])
            list_dokter = User.objects.filter(role='Dokter')
            list_hewan = Hewan.objects.filter(pemilik_id=my_uuid)

            if request.method == 'POST':
                form = AppointmentDokterForm(request.POST)
                print(form.errors)
                if form.is_valid():
                    appointment = form.save(commit=False)
                    hewan = form.cleaned_data['hewan']
                    if hewan:
                        appointment.hewan = hewan
                    cust_instance = Customer.objects.get(username=request.session["Username"])
                    appointment.pemilik = cust_instance
                    appointment.status = 'Menunggu Konfirmasi'
                    appointment.save()
                    success_message = 'Appointment kamu berhasil terbuat!'
                    return render(request, 'success_page_appt.html', {'success_message': success_message})
                    # return redirect('/appointmentdokter')
                else:
                    print("FORM ERROR:\n")
                    print(form.errors)
                    print("\nItu errornya di atas")
            else:
                form = AppointmentDokterForm()
            context = {
                    'listDokter': list_dokter,
                    'listHewan': list_hewan,
                    'form': form,
                    'user_id': my_uuid,
                    'username': my_username,
            }
            return render(request, 'create_appointmentdokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_appointmentdokter(request):
    if is_authenticated(request):
        my_username = request.session['Username']
        my_uuid = str(request.session['UUID'])
        if request.session['Role'] == 'Customer':
            list_appointmentdokter = AppointmentDokter.objects.filter(pemilik_id=my_uuid)
            list_disetujui_customer = AppointmentDokter.objects.filter(status='Disetujui', pemilik_id=my_uuid)
            list_konfirmasi_customer = AppointmentDokter.objects.filter(status='Menunggu Konfirmasi', pemilik_id=my_uuid)
            list_ditolak_customer = AppointmentDokter.objects.filter(status='Ditolak', pemilik_id=my_uuid)
            list_dibatalkan_customer = AppointmentDokter.objects.filter(status='Dibatalkan', pemilik_id=my_uuid)
            list_selesai_customer = AppointmentDokter.objects.filter(status='Selesai', pemilik_id=my_uuid)
            context = {
                'listAppointmentDokter': list_appointmentdokter,
                'list_disetujui': list_disetujui_customer,
                'list_konfirmasi': list_konfirmasi_customer,
                'list_ditolak': list_ditolak_customer,
                'list_dibatalkan': list_dibatalkan_customer,
                'list_selesai': list_selesai_customer,
                'username': my_username,
            }
            return render(request, 'listappointmentdok_customer.html', context)
        elif request.session['Role'] == 'Dokter':
            list_appointmentdokter = AppointmentDokter.objects.filter(dokter_id=my_uuid)
            list_disetujui_dokter = AppointmentDokter.objects.filter(status='Disetujui', dokter_id=my_uuid)
            list_konfirmasi_dokter = AppointmentDokter.objects.filter(status='Menunggu Konfirmasi', dokter_id=my_uuid)
            list_ditolak_dokter = AppointmentDokter.objects.filter(status='Ditolak', dokter_id=my_uuid)
            list_dibatalkan_dokter = AppointmentDokter.objects.filter(status='Dibatalkan', dokter_id=my_uuid)
            list_selesai_dokter = AppointmentDokter.objects.filter(status='Selesai', dokter_id=my_uuid)
            context = {
                'listAppointmentDokter': list_appointmentdokter,
                'list_disetujui': list_disetujui_dokter,
                'list_konfirmasi': list_konfirmasi_dokter,
                'list_ditolak': list_ditolak_dokter,
                'list_dibatalkan': list_dibatalkan_dokter,
                'list_selesai': list_selesai_dokter,
                'username': my_username,
            }
            return render(request, 'listappointmentdokter_dokter.html', context)
        else:
            list_appointmentdokter = AppointmentDokter.objects.all()
            context = {
                'listAppointmentDokter': list_appointmentdokter,
                'username': my_username,
            }
            
            return render(request, 'listappointmentdokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_disetujui(request):
    if is_authenticated(request):
        my_username = request.session['Username']
        my_uuid = str(request.session['UUID'])
        
        list_disetujui_customer = AppointmentDokter.objects.filter(status='Disetujui', pemilik_id=my_uuid)
        list_disetujui_dokter = AppointmentDokter.objects.filter(status='Disetujui', dokter_id=my_uuid)
        list_disetujui = AppointmentDokter.objects.filter(status='Disetujui')
        context = {
            'username': my_username,
            'listDisetujuiCustomer': list_disetujui_customer,
            'listDisetujuiDokter': list_disetujui_dokter,
            'listDisetujui': list_disetujui,
        }
        return render(request, 'listdisetujui.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_konfirmasi(request):
    if is_authenticated(request):
        my_username = request.session['Username']
        my_uuid = str(request.session['UUID'])
        
        list_konfirmasi_customer = AppointmentDokter.objects.filter(status='Menunggu Konfirmasi', pemilik_id=my_uuid)
        list_konfirmasi_dokter = AppointmentDokter.objects.filter(status='Menunggu Konfirmasi', dokter_id=my_uuid)
        list_konfirmasi = AppointmentDokter.objects.filter(status='Menunggu Konfirmasi')
        context = {
            'username': my_username,
            'listKonfirmasiCustomer': list_konfirmasi_customer,
            'listKonfirmasiDokter': list_konfirmasi_dokter,
            'listKonfirmasi': list_konfirmasi,
        }
        return render(request, 'listkonfirmasi.html', context)
    else:
        return HttpResponseRedirect("/login")

def list_ditolak(request):
    if is_authenticated(request):
        my_username = request.session['Username']
        my_uuid = str(request.session['UUID'])
        
        list_ditolak_customer = AppointmentDokter.objects.filter(status='Ditolak', pemilik_id=my_uuid)
        list_ditolak_dokter = AppointmentDokter.objects.filter(status='Ditolak', dokter_id=my_uuid)
        list_ditolak = AppointmentDokter.objects.filter(status='Ditolak')
        context = {
            'username': my_username,
            'listDitolakCustomer': list_ditolak_customer,
            'listDitolakDokter': list_ditolak_dokter,
            'listDitolak': list_ditolak,
        }
        return render(request, 'listditolak.html', context)
    else:
        return HttpResponseRedirect("/login")


def update_appointment(request, id):
    cursor = connection.cursor()
    username = request.session['Username']
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM appointmentdokter_appointmentdokter
    WHERE id = '{0}' ;
    """.format(id))
    appointmentdokter = cursor.fetchall()
    my_uuid = str(request.session['UUID'])
    list_dokter = User.objects.filter(role='Dokter')
    list_hewan = Hewan.objects.filter(pemilik_id=my_uuid)
        
    response = {
            'id':id,
            'appointmentdokter':appointmentdokter,
            'listDokter': list_dokter,
            'listHewan': list_hewan,
            'user_id': my_uuid,
            'username': username}
    cursor.close()
    return render(request, 'update_appointmentdokter.html', response)

def update_appointment_handler(request, id):
    if is_authenticated(request):
        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

        # get data dari form
        dokter = request.GET.get('dokter')
        hewan = request.GET.get('hewan')
        appointment_time = request.GET.get('appointment_time')
        keluhan = request.GET.get('keluhan')

        try:
            cursor.execute("""
            UPDATE appointmentdokter_appointmentdokter
            SET dokter_id = '{0}', hewan_id = '{1}', appointment_time = '{2}', keluhan = '{3}'
            WHERE id = '{4}';
            """.format(dokter, hewan, appointment_time, keluhan, id))                
            success_message = 'Data Appointment berhasil diubah!'
            cursor.close()
            return render(request, 'success_page_appt.html', {'success_message': success_message})
        except IntegrityError:
            # If the field is not unique, return an error message
            error_message = 'Error updating appointment.'
            cursor.execute("""
            SELECT *
            FROM appointmentdokter_appointmentdokter
            WHERE id = '{0}' ;
            """.format(id))
            appointmentdokter = cursor.fetchall()
            username = request.session['Username']
            response = {
                'error_message': error_message,
                'appointmentdokter':appointmentdokter,
                'id': id,
                'username': username}
            cursor.close()
                
            return render(request, 'update_appointmentdokter.html', response)

def read_appointmentdokter(request, apptdokter_id):
    response = {}
    if is_authenticated(request):
        uname = request.session['Username']
        appointment_dokter = AppointmentDokter.objects.get(appointment_id=apptdokter_id)
        print(appointment_dokter.appointment_id)
        print(appointment_dokter.pemilik_id)

        response['apptdokter'] = appointment_dokter

        customer = Customer.objects.get(id=appointment_dokter.pemilik_id)

        response['customer'] = customer
        
        customer_login = Customer
        if request.session['Role'] == 'Customer':
            # Fetch object Customer login
            user = User.objects.get(username=uname)
            customer_login = Customer.objects.get(user_ptr=user)
        if customer_login.id == appointment_dokter.pemilik_id or request.session['Role'] == 'Dokter': 
            # Fetch object Hewan
            hewan = Hewan.objects.get(hewan_id=appointment_dokter.hewan_id)

            response['hewan'] = hewan
            role = request.session['Role']
            response['role'] = role
            response['username'] = uname

            return render(request, 'read_appointmentdokter.html', response)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
        return render(request, 'error_page_apptdokter.html', context)

    else:
        return HttpResponseRedirect("/login")


def approve_appointmentdokter(request, apptdokter_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Dokter':

            status = "Disetujui"
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE appointmentdokter_appointmentdokter
                SET status = '{0}'
                WHERE appointment_id = '{1}';
                """.format(status, apptdokter_id)) 
            
            success_message = 'Berhasil menyetujui Appointment Dokter!'
            cursor.close()
            return render(request, 'success_page_appt.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_apptdokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def disapprove_appointmentdokter(request, apptdokter_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Dokter':

            status = "Ditolak"
            alasan = request.POST.get('alasan')
            print(alasan) 

            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE appointmentdokter_appointmentdokter
                SET status = '{0}'
                WHERE appointment_id = '{1}';
                """.format(status, apptdokter_id)) 
            
        
            success_message = 'Berhasil menolak Appointment Dokter!'
            cursor.close()
            return render(request, 'success_page_appt.html', {'success_message': success_message})
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_apptdokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def delete_appointmentdokter(request, apptdokter_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Customer':
            apptdokter = AppointmentDokter.objects.get(appointment_id=apptdokter_id)
            
            if apptdokter.status == "Menunggu Konfirmasi" or apptdokter.status == "Disetujui":
                status = "Dibatalkan"
                cursor = connection.cursor()
                cursor.execute("SET SEARCH_PATH TO PUBLIC;")

                cursor.execute("""
                    UPDATE appointmentdokter_appointmentdokter
                    SET status = '{0}'
                    WHERE appointment_id = '{1}';
                    """.format(status, apptdokter_id)) 

                success_message = 'Appointment Dokter dengan ID ' + apptdokter.appointment_id + ' berhasil dibatalkan!'
                context = {'success_message': success_message,
                            'apptdokter_id': apptdokter.appointment_id}
                return render(request, 'success_page_appt.html', {'success_message': success_message})
            else:
                context = {
                    'error_message': 'Tidak bisa membatalkan Appointment Grooming yang telah disetujui/ditolak.'}
                return render(request, 'error_page_apptdokter.html', context)
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_apptdokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def update_appointmentdokter(request, apptdokter_id):
    cursor = connection.cursor()
    cursor.execute("SET SEARCH_PATH TO PUBLIC;")

    # Mencari user
    cursor.execute("""
    SELECT *
    FROM appointmentdokter_appointmentdokter
    WHERE appointment_id = '{0}' ;
    """.format(apptdokter_id))
    appointmentdokter = cursor.fetchall()
    my_uuid = str(request.session['UUID'])
    list_dokter = User.objects.filter(role='Dokter')
    list_hewan = Hewan.objects.filter(pemilik_id=my_uuid)
        
    username = request.session['Username']
    response = {
            'apptdokter_id':apptdokter_id,
            'appointmentdokter':appointmentdokter,
            'listDokter': list_dokter,
            'listHewan': list_hewan,
            'user_id': my_uuid,
            'username': username}
    cursor.close()
    return render(request, 'update_appointmentdokter.html', response)

def update_appointment_handler(request, apptdokter_id):
    if is_authenticated(request):
        cursor = connection.cursor()
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")

        # get data dari form
        dokter = request.GET.get('dokter')
        hewan = request.GET.get('hewan')
        appointment_time = request.GET.get('appointment_time')
        keluhan = request.GET.get('keluhan')

        try:
            cursor.execute("""
            UPDATE appointmentdokter_appointmentdokter
            SET dokter_id = '{0}', hewan_id = '{1}', appointment_time = '{2}', keluhan = '{3}'
            WHERE appointment_id = '{4}';
            """.format(dokter, hewan, appointment_time, keluhan, apptdokter_id))                
            success_message = 'Data Appointment berhasil diubah!'
            cursor.close()
            return render(request, 'success_page_appt.html', {'success_message': success_message})
        except IntegrityError:
            # If the field is not unique, return an error message
            error_message = 'Error updating appointment.'
            cursor.execute("""
            SELECT *
            FROM appointmentdokter_appointmentdokter
            WHERE appointment_id = '{0}' ;
            """.format(apptdokter_id))
            appointmentdokter = cursor.fetchall()
            username = request.session['Username']
            response = {
                'error_message': error_message,
                'appointmentdokter':appointmentdokter,
                'apptdokter_id': apptdokter_id,
                'username': username}
            cursor.close()
                
            return render(request, 'update_appointmentdokter.html', response)


def finished_appointmentdokter(request, apptdokter_id):
    if is_authenticated(request):
        if request.session['Role'] == 'Dokter':

            status = "Selesai"
            cursor = connection.cursor()
            cursor.execute("SET SEARCH_PATH TO PUBLIC;")

            cursor.execute("""
                UPDATE appointmentdokter_appointmentdokter
                SET status = '{0}'
                WHERE appointment_id = '{1}';
                """.format(status, apptdokter_id)) 
            
            appointment = AppointmentDokter.objects.get(appointment_id=apptdokter_id)
            
        
            success_message = 'Appointment Dokter dengan ID ' + appointment.appointment_id + ' berhasil diselesaikan!'
            context = {'success_message': success_message,
                        'apptdokter_id': appointment.appointment_id}
            return render(request, 'success_page_appt.html', context)
                     
        else:
            context = {
            'error_message': 'Akses Ditolak!'}
            return render(request, 'error_page_apptdokter.html', context)
    else:
        return HttpResponseRedirect("/login")
