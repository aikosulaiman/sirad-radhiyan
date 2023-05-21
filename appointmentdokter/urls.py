from django.urls import path

from .views import *

urlpatterns = [
    path('', list_appointmentdokter, name='list_appointmentdokter'),
    path('create-appointmentdokter', create_appointmentdokter, name='create_appointmentdokter'),
    path('read-appointmentdokter/<str:apptdokter_id>', read_appointmentdokter, name='read_appointmentdokter'),
    path('approve-appointmentdokter/<str:apptdokter_id>', approve_appointmentdokter, name='approve_appointmentdokter'),
    path('disapprove-appointmentdokter/<str:apptdokter_id>', disapprove_appointmentdokter, name='disapprove_appointmentdokter'),
    path('delete-appointmentdokter/<str:apptdokter_id>', delete_appointmentdokter, name='delete_appointmentdokter'),
]