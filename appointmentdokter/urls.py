from django.urls import path

from .views import create_appointmentdokter

urlpatterns = [
    # path('', list_event, name='list_event'),
    path('create-appointmentdokter', create_appointmentdokter, name='create_appointmentdokter'),
]