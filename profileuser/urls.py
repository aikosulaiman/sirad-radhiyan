from django.urls import path
<<<<<<< HEAD
from .views import index, update_profile, update_profile_handler, update_hewan, update_hewan_handler, read_profile
=======
from .views import index, update_profile, update_profile_handler, update_hewan, update_hewan_handler
>>>>>>> 20adbe49d1164b3cdaa7dba2724d3ce4c546b6a8

urlpatterns = [
    path('', index, name='Index'),
    path('update-profile/<uuid:user_id>', update_profile, name='update_profile'),
    path('update-profile-handler/<uuid:user_id>', update_profile_handler, name='update_profile_handler'),
    path('update-hewan/<int:user_id>', update_hewan, name='update_hewan'),
<<<<<<< HEAD
    path('update-hewan-handler/<int:user_id>', update_hewan_handler, name='update_hewan_handler'),
    path('read-profile/', read_profile, name='Read Profile')
=======
    path('update-hewan-handler/<int:user_id>', update_hewan_handler, name='update_hewan_handler')
>>>>>>> 20adbe49d1164b3cdaa7dba2724d3ce4c546b6a8
]
