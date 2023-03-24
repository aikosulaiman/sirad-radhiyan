from django.urls import path
from .views import index, update_profile, update_profile_handler, update_hewan, update_hewan_handler, read_profile

urlpatterns = [
    path('', index, name='Index'),
    path('update-profile/<uuid:user_id>', update_profile, name='update_profile'),
    path('update-profile-handler/<uuid:user_id>', update_profile_handler, name='update_profile_handler'),
    path('update-hewan/<int:user_id>', update_hewan, name='update_hewan'),
    path('update-hewan-handler/<int:user_id>', update_hewan_handler, name='update_hewan_handler'),
    path('read-profile/<str:username>', read_profile, name='read_profile')
]