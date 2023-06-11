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
        cursor.execute("""
    SELECT EXTRACT(MONTH FROM ra.date_adopted) AS month, a.jenis, COUNT(*) AS count
    FROM adopsi_register_adopsi ra
    JOIN adopsi_adopsi a ON ra.hewan_id = a.hewan_id
    WHERE ra.status = 'Disetujui'
    GROUP BY EXTRACT(MONTH FROM ra.date_adopted), a.jenis
    ORDER BY EXTRACT(MONTH FROM ra.date_adopted)
""")
        adopted = cursor.fetchall()
        print(adopted)
        for i in adopted:
            print(i[0])
            print(i[1])

        # Format the data for the chart
        month_names = []
        jenis_hewan = []
        adopted_counts = []
        for adopt in adopted:
            month = adopt[0]
            jenis = adopt[1]
            count = adopt[2]
            month_names.append(month)
            jenis_hewan.append(jenis)
            adopted_counts.append(count)
        print(month_names)
        print(jenis_hewan)
        print(adopted_counts)

        labels_json = json.dumps(month_names, default=str)

        print(labels_json)

        nama_bulan = []
        janKCount = 0
        febKCount = 0
        marKCount = 0
        aprKCount = 0
        meiKCount = 0
        junKCount = 0
        julKCount = 0
        augKCount = 0
        sepKCount = 0
        oktKCount = 0
        novKCount = 0
        desKCount = 0

        janACount = 0
        febACount = 0
        marACount = 0
        aprACount = 0
        meiACount = 0
        junACount = 0
        julACount = 0
        augACount = 0
        sepACount = 0
        oktACount = 0
        novACount = 0
        desACount = 0

        janLCount = 0
        febLCount = 0
        marLCount = 0
        aprLCount = 0
        meiLCount = 0
        junLCount = 0
        julLCount = 0
        augLCount = 0
        sepLCount = 0
        oktLCount = 0
        novLCount = 0
        desLCount = 0

        kucingCounts = []
        anjingCounts = []
        kelinciCounts = []
        
        for label in adopted:
            print(label[0])
            if label[0] == 1:
                nama_bulan.append("Januari")
                if label[1] == 'Kucing':
                    janKCount = label[2]
                elif label[1] == 'Anjing':
                    janACount = label[2]
                elif label[1] == 'Kelinci':
                    janLCount = label[2]
            elif label[0] == 2:
                nama_bulan.append("Februari")
                if label[1] == 'Kucing':
                    febKCount = label[2]
                elif label[1] == 'Anjing':
                    febACount = label[2]
                elif label[1] == 'Kelinci':
                    febLCount = label[2]
            elif label[0] == 3:
                nama_bulan.append("Maret")
                if label[1] == 'Kucing':
                    marKCount = label[2]
                elif label[1] == 'Anjing':
                    marACount = label[2]
                elif label[1] == 'Kelinci':
                    marLCount = label[2]
            elif label[0] == 4:
                nama_bulan.append("April")
                if label[1] == 'Kucing':
                    aprKCount = label[2]
                elif label[1] == 'Anjing':
                    aprACount = label[2]
                elif label[1] == 'Kelinci':
                    aprLCount = label[2]
            elif label[0] == 5:
                nama_bulan.append("Mei")
                if label[1] == 'Kucing':
                    meiKCount = label[2]
                elif label[1] == 'Anjing':
                    meiACount = label[2]
                elif label[1] == 'Kelinci':
                    meiLCount = label[2]
            elif label[0] == 6:
                nama_bulan.append("Juni")
                if label[1] == 'Kucing':
                    junKCount = label[2]
                elif label[1] == 'Anjing':
                    junACount = label[2]
                elif label[1] == 'Kelinci':
                    junLCount = label[2]
            elif label[0] == 7:
                nama_bulan.append("Juli")
                if label[1] == 'Kucing':
                    julKCount = label[2]
                elif label[1] == 'Anjing':
                    julACount = label[2]
                elif label[1] == 'Kelinci':
                    julLCount = label[2]
            elif label[0] == 8:
                nama_bulan.append("Agustus")
                if label[1] == 'Kucing':
                    augKCount = label[2]
                elif label[1] == 'Anjing':
                    augACount = label[2]
                elif label[1] == 'Kelinci':
                    augLCount = label[2]
            elif label[0] == 9:
                nama_bulan.append("September")
                if label[1] == 'Kucing':
                    sepKCount = label[2]
                elif label[1] == 'Anjing':
                    sepACount = label[2]
                elif label[1] == 'Kelinci':
                    sepLCount = label[2]
            elif label[0] == 10:
                nama_bulan.append("Oktober")
                if label[1] == 'Kucing':
                    oktKCount = label[2]
                elif label[1] == 'Anjing':
                    oktACount = label[2]
                elif label[1] == 'Kelinci':
                    oktLCount = label[2]
            elif label[0] == 11:
                nama_bulan.append("November")
                if label[1] == 'Kucing':
                    novKCount = label[2]
                elif label[1] == 'Anjing':
                    novACount = label[2]
                elif label[1] == 'Kelinci':
                    novLCount = label[2]
            elif label[0] == 12:
                nama_bulan.append("Desember")
                if label[1] == 'Kucing':
                    desKCount = label[2]
                elif label[1] == 'Anjing':
                    desACount = label[2]
                elif label[1] == 'Kelinci':
                    desLCount = label[2]

        kucingCounts.append(janKCount)
        kucingCounts.append(febKCount)
        kucingCounts.append(marKCount)
        kucingCounts.append(aprKCount)
        kucingCounts.append(meiKCount)
        kucingCounts.append(junKCount)
        kucingCounts.append(julKCount)
        kucingCounts.append(augKCount)
        kucingCounts.append(sepKCount)
        kucingCounts.append(oktKCount)
        kucingCounts.append(novKCount)
        kucingCounts.append(desKCount)

        anjingCounts.append(janACount)
        anjingCounts.append(febACount)
        anjingCounts.append(marACount)
        anjingCounts.append(aprACount)
        anjingCounts.append(meiACount)
        anjingCounts.append(junACount)
        anjingCounts.append(julACount)
        anjingCounts.append(augACount)
        anjingCounts.append(sepACount)
        anjingCounts.append(oktACount)
        anjingCounts.append(novACount)
        anjingCounts.append(desACount)

        kelinciCounts.append(janLCount)
        kelinciCounts.append(febLCount)
        kelinciCounts.append(marLCount)
        kelinciCounts.append(aprLCount)
        kelinciCounts.append(meiLCount)
        kelinciCounts.append(junLCount)
        kelinciCounts.append(julLCount)
        kelinciCounts.append(augLCount)
        kelinciCounts.append(sepLCount)
        kelinciCounts.append(oktLCount)
        kelinciCounts.append(novLCount)
        kelinciCounts.append(desLCount)

        set_bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
 
        labels_json_namabulan = json.dumps(set_bulan, default=str)
        labels_json_kucingcount = json.dumps(kucingCounts)
        labels_json_anjingcount = json.dumps(anjingCounts)
        labels_json_kelincicount = json.dumps(kelinciCounts)

        context = {
        'month_names': labels_json_namabulan,
        'kucing_counts': labels_json_kucingcount,
        'anjing_counts': labels_json_anjingcount,
        'kelinci_counts': labels_json_kelincicount,
        }

        return render(request, 'statistik_adopsi.html', context)
    else:
        return HttpResponseRedirect("/login")
    
def statistik_grooming(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
        COUNT(*) FROM appointmentgrooming_appointmentgrooming 
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
            
        labels_json_namabulan = json.dumps(nama_bulan, default=str)

        context = {
        'month_names': labels_json_namabulan,
        'appointment_counts': data_json,
    }

        return render(request, 'statistik_grooming.html', context)
    else:
        return HttpResponseRedirect("/login")
