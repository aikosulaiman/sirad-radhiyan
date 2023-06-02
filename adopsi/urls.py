from django.urls import path
from .views import *

urlpatterns = [
    path('', list_hewan_adopsi, name='list_hewan_adopsi'),
    path('create-adopsi', create_adopsi, name='create_adopsi'),
    path('update-adopsi/<uuid:user_id>', update_adopsi, name='update_adopsi'),
    path('update-adopsi-handler/<uuid:user_id>', update_adopsi_handler, name='update_adopsi_handler'),
    path('delete-adopsi/<uuid:hewan_id>', delete_adopsi, name='delete_adopsi'),
    path('read-adopsi/<uuid:hewan_id>', read_adopsi, name='read_adopsi'),
    path('register-adopsi/<uuid:hewan_id>', register_adopsi, name='register_adopsi'),
    path('list-adopsi-customer', list_adopsi_customer, name='list_adopsi_customer'),
    path('approve-adopsi/<uuid:hewan_id>/<str:id>', approve_adopsi, name='approve_adopsi'),
    path('disapprove-adopsi/<uuid:hewan_id>/<str:id>', disapprove_adopsi, name='disapprove_adopsi'),
]