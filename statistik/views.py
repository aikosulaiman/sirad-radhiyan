from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import connection
from django.db.models import Count
from django.core import serializers
import json
from events.models import Event, Register_Event

from user.models import User, Customer, Dokter, Hewan
from appointmentdokter.models import AppointmentDokter

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def statistik_dokter(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
        COUNT(*) FROM appointmentdokter_appointmentdokter 
        GROUP BY EXTRACT(MONTH FROM appointment_time)
        ORDER BY EXTRACT(MONTH FROM appointment_time)
        """)
        appointments = cursor.fetchall()
        print(appointments)
        for i in appointments:
            print(i[0])
            print(i[1])

        # Format the data for the chart
        month_names = []
        appointment_counts = []
        for appointment in appointments:
            # appointment_date = appointment[0]
            # month = appointment_date.strftime('%B')  # Get the month name
            month = appointment[0]
            count = appointment[1]
            month_names.append(month)
            appointment_counts.append(count)
        print(month_names)
        print(appointment_counts)

        labels_json = json.dumps(month_names, default=str)
        data_json = json.dumps(appointment_counts)

        print(labels_json)

        nama_bulan = []
        for label in labels_json:
            if label == '1':
                nama_bulan.append("Januari")
            elif label == '2':
                nama_bulan.append("Februari")
            elif label == '3':
                nama_bulan.append("Maret")
            elif label == '4':
                nama_bulan.append("April")
            elif label == '5':
                nama_bulan.append("Mei")
            elif label == '6':
                nama_bulan.append("Juni")
            elif label == '7':
                nama_bulan.append("Juli")
            elif label == '8':
                nama_bulan.append("Agustus")
            elif label == '9':
                nama_bulan.append("September")
            elif label == '10':
                nama_bulan.append("Oktober")
            elif label == '11':
                nama_bulan.append("November")
            elif label == '12':
                nama_bulan.append("Desember")

        print(nama_bulan)
        print(data_json)
            
        labels_json_namabulan = json.dumps(nama_bulan, default=str)

        context = {
        'month_names': labels_json_namabulan,
        'appointment_counts': data_json,
    }

        return render(request, 'statistik_dokter.html', context)
    else:
        return HttpResponseRedirect("/login")

def statistik_event(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT jenis, quantity
        FROM events_event
        """)
        events = cursor.fetchall()
        
        jenis_names = []
        events_counts = []
        for event in events:
            # appointment_date = appointment[0]
            # month = appointment_date.strftime('%B')  # Get the month name
            jenis = event[0]
            count = event[1]
            jenis_names.append(jenis)
            events_counts.append(count)
        print(jenis_names)
        print(events_counts)


        steril_count = 0
        vaksin_count = 0
        sem_count = 0
        sale_count = 0
        lomba_count = 0
        bazaar_count = 0
        event_count = 0
        nama_jenis = ['Sterilisasi', 'Vaksinasi', 'Seminar/Webinar', 'Promo/Sale', 'Lomba', 'Bazaar','Special Event']
    
        countTemp = 0
        for temp in events_counts:
            if jenis_names[countTemp] == 'Sterilisasi':
                steril_count = steril_count+temp
            elif jenis_names[countTemp] == 'Vaksinasi':
                vaksin_count = vaksin_count+temp
            elif jenis_names[countTemp] == 'Seminar/Webinar':
                sem_count = sem_count+temp
            elif jenis_names[countTemp] == 'Promo/Sale':
                sale_count = sale_count+temp
            elif jenis_names[countTemp] == 'Lomba':
                lomba_count = lomba_count+temp
            elif jenis_names[countTemp] == 'Bazaar':
                bazaar_count = bazaar_count+temp
            elif jenis_names[countTemp] == 'Special Event':
                event_count = event_count+temp
            countTemp = countTemp+1

        total_pendaftar = []
        total_pendaftar.append(steril_count)
        total_pendaftar.append(vaksin_count)
        total_pendaftar.append(sem_count)
        total_pendaftar.append(sale_count)
        total_pendaftar.append(lomba_count)
        total_pendaftar.append(bazaar_count)
        total_pendaftar.append(event_count)
            
        labels_json_namajenis = json.dumps(nama_jenis, default=str)
        labels_json_pendaftarcount = json.dumps(total_pendaftar, default=str)

        all_event = Event.objects.all().values

        context = {
        'all_event':all_event,
        'jenis_names': labels_json_namajenis,
        'events_counts': labels_json_pendaftarcount,
    }

        return render(request, 'statistik_event.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def statistik_adopsi(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT EXTRACT(MONTH FROM date_adopted), 
        COUNT(*) FROM adopsi_register_adopsi WHERE status='Disetujui'
        GROUP BY EXTRACT(MONTH FROM date_adopted)
        ORDER BY EXTRACT(MONTH FROM date_adopted)
        """)
        adopted = cursor.fetchall()
        print(adopted)
        for i in adopted:
            print(i[0])
            print(i[1])

        # Format the data for the chart
        month_names = []
        adopted_counts = []
        for adopt in adopted:
            month = adopt[0]
            count = adopt[1]
            month_names.append(month)
            adopted_counts.append(count)
        print(month_names)
        print(adopted_counts)

        labels_json = json.dumps(month_names, default=str)
        data_json = json.dumps(adopted_counts)

        print(labels_json)

        nama_bulan = []
        for label in labels_json:
            if label == '1':
                nama_bulan.append("Januari")
            elif label == '2':
                nama_bulan.append("Februari")
            elif label == '3':
                nama_bulan.append("Maret")
            elif label == '4':
                nama_bulan.append("April")
            elif label == '5':
                nama_bulan.append("Mei")
            elif label == '6':
                nama_bulan.append("Juni")
            elif label == '7':
                nama_bulan.append("Juli")
            elif label == '8':
                nama_bulan.append("Agustus")
            elif label == '9':
                nama_bulan.append("September")
            elif label == '10':
                nama_bulan.append("Oktober")
            elif label == '11':
                nama_bulan.append("November")
            elif label == '12':
                nama_bulan.append("Desember")

        print(nama_bulan)
        print(data_json)
            
        labels_json_namabulan = json.dumps(nama_bulan, default=str)

        context = {
        'month_names': labels_json_namabulan,
        'adopted_counts': data_json,
    }

        return render(request, 'statistik_adopsi.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def statistik_grooming(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT up.nama, COUNT(*)
        FROM user_produk AS up
        JOIN appointmentgrooming_appointmentgrooming AS ag 
        ON ag.paket_id = up.id
        JOIN appointmentgrooming_appointmentgrooming_layanan_tambahan AS lt 
        ON lt.appointmentgrooming_id = ag.id
        GROUP BY up.nama;
        """)
        list_master_data = cursor.fetchall()
        print(list_master_data)
        for i in list_master_data:
            print(i[0])
            print(i[1])

        # Format the data for the chart
        master_data = []
        appointment_counts = []
        for appointment in list_master_data:
            month = appointment[0]
            count = appointment[1]
            master_data.append(month)
            appointment_counts.append(count)
        print(master_data)
        print(appointment_counts)

        labels_json = json.dumps(master_data, default=str)
        data_json = json.dumps(appointment_counts)

        print(labels_json)

        context = {
        'master_data': labels_json,
        'appointment_counts': data_json,
    }

        return render(request, 'statistik_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")
