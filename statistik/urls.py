from django.urls import path

from .views import *

urlpatterns = [
    path('statistik-dokter', statistik_dokter, name='statistik_dokter'),
    path('statistik-event', statistik_event, name='statistik_event'),
]