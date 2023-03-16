from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('customer-registration/', views.customer_registration, name="Customer Registration"),
]