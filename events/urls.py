from django.urls import path

from .views import create_event, list_event, update_event, update_event_handler

urlpatterns = [
    path('', list_event, name='list_event'),
    path('create-event', create_event, name='create_event'),
    path('update-event/<uuid:event_id>', update_event, name='update_event'),
    path('update-event-handler/<uuid:event_id>', update_event_handler, name='update_event_handler'),
]