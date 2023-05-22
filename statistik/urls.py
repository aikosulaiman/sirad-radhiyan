from django.urls import path

from .views import *

urlpatterns = [
    path('statistik-dokter', statistik_dokter, name='statistik_dokter'),
    path('statistik-event', statistik_event, name='statistik_event'),
    path('statistik-adopsi', statistik_adopsi, name='statistik_adopsi'),
]