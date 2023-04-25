from django.urls import path

from .views import *

urlpatterns = [
    path('', list_appointmentdokter, name='list_appointmentdokter'),
    path('create-appointmentdokter', create_appointmentdokter, name='create_appointmentdokter'),
]