from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import connection

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

            print(list_dokter)
            print(list_hewan)


            if request.method == 'POST':
                form = AppointmentDokterForm(request.POST)
                print(form.errors)
                if form.is_valid():
                    appointment = form.save(commit=False)
                    # last_id = AppointmentDokter.objects.order_by('-id').first()
                    # if last_id:
                    #     last_id = int(last_id.id[6:])
                    # else:
                    #     last_id = 0
                    # appointment.id = 'APTDOC' + str(last_id + 1).zfill(6)
                    print(form.cleaned_data)
                    print('ngetest')
                    hewan = form.cleaned_data['hewan']
                    if hewan:
                        appointment.hewan = hewan
                    print(hewan)
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
            context = {
                'listAppointmentDokter': list_appointmentdokter,
                'username': my_username,
            }
            return render(request, 'listappointmentdok_customer.html', context)
        elif request.session['Role'] == 'Dokter':
            list_appointmentdokter = AppointmentDokter.objects.filter(dokter_id=my_uuid)
            context = {
                'listAppointmentDokter': list_appointmentdokter,
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


def read_appointmentdokter(request, apptdokter_id):
    response = {}
    if is_authenticated(request):
        appointment_dokter = AppointmentDokter.objects.get(appointment_id=apptdokter_id)
        print(appointment_dokter.appointment_id)
        print(appointment_dokter.pemilik_id)

        response['apptdokter'] = appointment_dokter

        customer = Customer.objects.get(id=appointment_dokter.pemilik_id)

        response['customer'] = customer
        
        customer_login = Customer
        if request.session['Role'] == 'Customer':
            # Fetch object Customer login
            uname = request.session['Username']
            user = User.objects.get(username=uname)
            customer_login = Customer.objects.get(user_ptr=user)
        if customer_login.id == appointment_dokter.pemilik_id or request.session['Role'] == 'Dokter': 
            # Fetch object Hewan
            hewan = Hewan.objects.get(hewan_id=appointment_dokter.hewan_id)

            response['hewan'] = hewan
            role = request.session['Role']
            response['role'] = role

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
            
            if apptdokter.status == "Menunggu Konfirmasi":
                apptdokter.delete()
                success_message = 'Berhasil membatalkan Appointment Dokter!'
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
