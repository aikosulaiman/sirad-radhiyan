from django.urls import path
from . import views

urlpatterns = [
    path('customer-registration/', views.customer_registration, name="Customer Registration"),
    path('', views.index, name='Index'),
    path('form-pendaftaran-hewan/', views.form_pendaftaran_hewan, name="Form Pendaftaran Hewan"),
    path('payment-form/', views.payment_form, name="Payment Form"),
]