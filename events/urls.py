from django.urls import path

from .views import *

urlpatterns = [
    path('', list_event, name='list_event'),
    path('create-event', create_event, name='create_event'),
    path('update-event/<uuid:event_id>', update_event, name='update_event'),
    path('update-event-handler/<uuid:event_id>', update_event_handler, name='update_event_handler'),
    path('read-event/<uuid:event_id>', read_event, name='read_event'),
    path('register-event/<uuid:event_id>', register_event, name='register_event'),
]