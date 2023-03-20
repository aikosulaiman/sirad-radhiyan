from django.urls import path

from .views import create_event, list_event

urlpatterns = [
    path('', list_event, name='list_event'),
    path('create-event', create_event, name='create_event'),
]