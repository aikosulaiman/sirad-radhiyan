from django.urls import path
from .views import index, update_profile, update_profile_handler, customer_registration, form_pendaftaran_hewan, payment_form, update_hewan, update_hewan_handler

urlpatterns = [
    path('', index, name='Index'),
    path('update-profile/<uuid:user_id>', update_profile, name='update_profile'),
    path('update-profile-handler/<uuid:user_id>', update_profile_handler, name='update_profile_handler'),
    path('customer-registration/', customer_registration, name="Customer Registration"),
    path('form-pendaftaran-hewan/', form_pendaftaran_hewan, name="Form Pendaftaran Hewan"),
    path('payment-form/', payment_form, name="Payment Form"),
    path('update-hewan/<int:user_id>', update_hewan, name='update_hewan'),
    path('update-hewan-handler/<int:user_id>', update_hewan_handler, name='update_hewan_handler')
]
