from django.urls import path

from .views import *

urlpatterns = [
    path('statistik', statistik, name='statistik'),
    # path('statistik-dokter', statistik_dokter, name='statistik_dokter'),
    # path('statistik-grooming', statistik_grooming, name='statistik_grooming'),
]