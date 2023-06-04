from django.urls import path

from .views import *

urlpatterns = [
    path('', list_appointmentdokter, name='list_appointmentdokter'),
    path('create-appointmentdokter', create_appointmentdokter, name='create_appointmentdokter'),
    path('update-appointmentdokter/<int:id>', update_appointment, name='update_appointment'),
    path('update-appointmentdokter-handler/<int:id>', update_appointment_handler, name='update_appointment_handler'),
    path('read-appointmentdokter/<str:apptdokter_id>', read_appointmentdokter, name='read_appointmentdokter'),
    path('approve-appointmentdokter/<str:apptdokter_id>', approve_appointmentdokter, name='approve_appointmentdokter'),
    path('disapprove-appointmentdokter/<str:apptdokter_id>', disapprove_appointmentdokter, name='disapprove_appointmentdokter'),
    path('delete-appointmentdokter/<str:apptdokter_id>', delete_appointmentdokter, name='delete_appointmentdokter'),
    path('disetujui', list_disetujui, name='list_disetujui'),
    path('konfirmasi', list_konfirmasi, name='list_konfirmasi'),
    path('ditolak', list_ditolak, name='list_ditolak'),
    path('update-appointmentdokter/<str:apptdokter_id>', update_appointmentdokter, name='update_appointmentdokter'),
    path('update-appointment-handler/<str:apptdokter_id>', update_appointment_handler, name='update_appointment_handler'),
    path('finished-appointmentdokter/<str:apptdokter_id>', finished_appointmentdokter, name='finished_appointmentdokter'),
]