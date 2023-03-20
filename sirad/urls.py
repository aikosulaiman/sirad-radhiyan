from django.urls import path
from . import views

urlpatterns = [
    path('customer-registration/', views.customer_registration, name="Customer Registration"),
    path('', views.index, name='Index'),
    path('signup-form/', views.signup_form, name="Signup Form"),
    path('payment-form/', views.payment_form, name="Payment Form"),
]