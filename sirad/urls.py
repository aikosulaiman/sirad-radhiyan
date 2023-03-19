from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('read-profile/', views.read_profile, name='Read Profile')
]