from django.shortcuts import render, redirect
import datetime
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta, timezone
from django.contrib import messages
from django.db import connection
from django.db.models import Count
from django.core import serializers
import json

from user.models import User, Customer, Dokter, Hewan
from appointmentdokter.models import AppointmentDokter

def is_authenticated(request):
    try:
        request.session['Username']
        return True
    except:
        return False

def statistik(request):
    cursor = connection.cursor()
    if is_authenticated(request):
        cursor.execute("SET SEARCH_PATH TO PUBLIC;")
        cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
        COUNT(*) FROM appointmentdokter_appointmentdokter 
        GROUP BY EXTRACT(MONTH FROM appointment_time)
        ORDER BY EXTRACT(MONTH FROM appointment_time)
        """)
        appointment_dokter = cursor.fetchall()

        cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
        COUNT(*) FROM appointmentgrooming_appointmentgrooming 
        GROUP BY EXTRACT(MONTH FROM appointment_time)
        ORDER BY EXTRACT(MONTH FROM appointment_time)
        """)
        appointment_grooming = cursor.fetchall()

        print(appointment_dokter)
        for i in appointment_dokter:
            print(i[0])
            print(i[1])

        print(appointment_grooming)
        for i in appointment_grooming:
            print(i[0])
            print(i[1])

        # Format the data for the chart
        month_names = []
        appointment_dokter_counts = []
        appointment_grooming_counts = []
        for appointment in appointment_dokter:
            month = appointment[0]
            count = appointment[1]
            month_names.append(month)
            appointment_dokter_counts.append(count)

        for appointment in appointment_grooming:
            count = appointment[1]
            appointment_grooming_counts.append(count)

        print(month_names)
        print(appointment_dokter_counts)
        print(appointment_grooming_counts)

        labels_json = json.dumps(month_names, default=str)
        data_dokter_json = json.dumps(appointment_dokter_counts)
        data_grooming_json = json.dumps(appointment_grooming_counts)

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
        'appointment_dokter_counts': data_dokter_json,
        'appointment_grooming_counts': data_grooming_json,
    }

        return render(request, 'statistik.html', context)
    else:
        return HttpResponseRedirect("/login")

# def statistik_dokter(request):
#     cursor = connection.cursor()
#     if is_authenticated(request):
#         cursor.execute("SET SEARCH_PATH TO PUBLIC;")
#         cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
#         COUNT(*) FROM appointmentdokter_appointmentdokter 
#         GROUP BY EXTRACT(MONTH FROM appointment_time)
#         ORDER BY EXTRACT(MONTH FROM appointment_time)
#         """)
#         appointments = cursor.fetchall()
        # print(appointments)
        # for i in appointments:
        #     print(i[0])
        #     print(i[1])

#         # Format the data for the chart
#         month_names = []
#         appointment_counts = []
#         for appointment in appointments:
#             # appointment_date = appointment[0]
#             # month = appointment_date.strftime('%B')  # Get the month name
#             month = appointment[0]
#             count = appointment[1]
#             month_names.append(month)
#             appointment_counts.append(count)
#         print(month_names)
#         print(appointment_counts)

#         labels_json = json.dumps(month_names, default=str)
#         data_json = json.dumps(appointment_counts)

#         print(labels_json)

#         nama_bulan = []
#         for label in labels_json:
#             if label == '1':
#                 nama_bulan.append("Januari")
#             elif label == '2':
#                 nama_bulan.append("Februari")
#             elif label == '3':
#                 nama_bulan.append("Maret")
#             elif label == '4':
#                 nama_bulan.append("April")
#             elif label == '5':
#                 nama_bulan.append("Mei")
#             elif label == '6':
#                 nama_bulan.append("Juni")
#             elif label == '7':
#                 nama_bulan.append("Juli")
#             elif label == '8':
#                 nama_bulan.append("Agustus")
#             elif label == '9':
#                 nama_bulan.append("September")
#             elif label == '10':
#                 nama_bulan.append("Oktober")
#             elif label == '11':
#                 nama_bulan.append("November")
#             elif label == '12':
#                 nama_bulan.append("Desember")

#         print(nama_bulan)
            
#         labels_json_namabulan = json.dumps(nama_bulan, default=str)

#         context = {
#         'month_names': labels_json_namabulan,
#         'appointment_counts': data_json,
#     }

#         return render(request, 'statistik_dokter.html', context)
#     else:
#         return HttpResponseRedirect("/login")

# def statistik_grooming(request):
#     cursor = connection.cursor()
#     if is_authenticated(request):
#         cursor.execute("SET SEARCH_PATH TO PUBLIC;")
#         cursor.execute("""SELECT EXTRACT(MONTH FROM appointment_time), 
#         COUNT(*) FROM appointmentgrooming_appointmentgrooming 
#         GROUP BY EXTRACT(MONTH FROM appointment_time)
#         ORDER BY EXTRACT(MONTH FROM appointment_time)
#         """)
#         appointments = cursor.fetchall()
#         print(appointments)
#         for i in appointments:
#             print(i[0])
#             print(i[1])

#         # Format the data for the chart
#         month_names = []
#         appointment_counts = []
#         for appointment in appointments:
#             # appointment_date = appointment[0]
#             # month = appointment_date.strftime('%B')  # Get the month name
#             month = appointment[0]
#             count = appointment[1]
#             month_names.append(month)
#             appointment_counts.append(count)
#         print(month_names)
#         print(appointment_counts)

#         labels_json = json.dumps(month_names, default=str)
#         data_json = json.dumps(appointment_counts)

#         print(labels_json)

#         nama_bulan = []
#         for label in labels_json:
#             if label == '1':
#                 nama_bulan.append("Januari")
#             elif label == '2':
#                 nama_bulan.append("Februari")
#             elif label == '3':
#                 nama_bulan.append("Maret")
#             elif label == '4':
#                 nama_bulan.append("April")
#             elif label == '5':
#                 nama_bulan.append("Mei")
#             elif label == '6':
#                 nama_bulan.append("Juni")
#             elif label == '7':
#                 nama_bulan.append("Juli")
#             elif label == '8':
#                 nama_bulan.append("Agustus")
#             elif label == '9':
#                 nama_bulan.append("September")
#             elif label == '10':
#                 nama_bulan.append("Oktober")
#             elif label == '11':
#                 nama_bulan.append("November")
#             elif label == '12':
#                 nama_bulan.append("Desember")

#         print(nama_bulan)
            
#         labels_json_namabulan = json.dumps(nama_bulan, default=str)

#         context = {
#         'month_names': labels_json_namabulan,
#         'appointment_counts': data_json,
#     }

#         return render(request, 'statistik_grooming.html', context)
#     else:
#         return HttpResponseRedirect("/login")