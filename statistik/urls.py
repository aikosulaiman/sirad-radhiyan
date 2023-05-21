from django.urls import path

from .views import *

urlpatterns = [
    path('statistik-dokter', statistik_dokter, name='statistik_dokter'),
]