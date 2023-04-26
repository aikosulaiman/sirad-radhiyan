from django.urls import path
from .views import create_adopsi, list_hewan_adopsi, update_adopsi, update_adopsi_handler, read_adopsi

urlpatterns = [
    path('', list_hewan_adopsi, name='list_hewan_adopsi'),
    path('create-adopsi', create_adopsi, name='create_adopsi'),
    path('read-adopsi/<uuid:hewan_id>', read_adopsi, name='read_adopsi'),
    # path('read-adopsi/<uuid:user_id>', read_adopsi, name='read_adopsi'),
    path('update-adopsi/<uuid:user_id>', update_adopsi, name='update_adopsi'),
    path('update-adopsi-handler/<uuid:user_id>', update_adopsi_handler, name='update_adopsi_handler'),
]