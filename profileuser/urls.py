from django.urls import path
from .views import index, update_profile, update_profile_handler, update_hewan, update_hewan_handler, read_profile, submit_vip_validation, tambah_hewan, tambah_hewan_handler, delete_hewan 

urlpatterns = [
    path('', index, name='Index'),
    path('update-profile/<uuid:user_id>', update_profile, name='update_profile'),
    path('update-profile-handler/<uuid:user_id>', update_profile_handler, name='update_profile_handler'),
    # path('form-pendaftaran-hewan/', form_pendaftaran_hewan, name="form_pendaftaran_hewan"),
    # path('payment-form/', payment_form, name="Payment Form"),
    path('update-hewan/<int:user_id>', update_hewan, name='update_hewan'),
    path('update-hewan-handler/<int:user_id>', update_hewan_handler, name='update_hewan_handler'),
    path('read-profile/<str:username>', read_profile, name='read_profile'),
    path('submit-vip-validation/<uuid:user_id>', submit_vip_validation, name='submit_vip_validation'),
    path('tambah-hewan/<uuid:user_id>', tambah_hewan, name='tambah_hewan'),
    path('tambah-hewan-handler/<uuid:user_id>', tambah_hewan_handler, name='tambah_hewan_handler'),
    path('delete-hewan/<int:hewan_id>', delete_hewan, name='delete_hewan'),
]