from sqlite3 import IntegrityError
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

def update_appointment(request, id):
    cursor = connection.cursor()
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
            'user_id': my_uuid,}
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
            response = {
                'error_message': error_message,
                'appointmentdokter':appointmentdokter,
                'id': id}
            cursor.close()
                
            return render(request, 'update_appointmentdokter.html', response)