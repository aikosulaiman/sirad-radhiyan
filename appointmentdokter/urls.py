from django.urls import path

from .views import *

urlpatterns = [
    path('', list_appointmentdokter, name='list_appointmentdokter'),
    path('create-appointmentdokter', create_appointmentdokter, name='create_appointmentdokter'),
    path('update-appointmentdokter/<int:id>', update_appointment, name='update_appointment'),
    path('update-appointmentdokter-handler/<int:id>', update_appointment_handler, name='update_appointment_handler'),

]