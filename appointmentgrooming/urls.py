from django.urls import path

from .views import *

urlpatterns = [
    path('', list_appointmentgrooming, name='list_appointmentgrooming'),
    path('create-appointmentgrooming', create_appointmentgrooming, name='create_appointmentgrooming'),
    path('read-appointmentgrooming/<int:apptgrooming_id>', read_appointmentgrooming, name='read_appointmentgrooming'),
    path('approve-appointmentgrooming/<int:apptgrooming_id>', approve_appointmentgrooming, name='approve_appointmentgrooming'),
    path('disapprove-appointmentgrooming/<int:apptgrooming_id>', disapprove_appointmentgrooming, name='disapprove_appointmentgrooming'),
    path('update-appointmentgrooming/<int:apptgrooming_id>', update_appointmentgrooming, name='update_appointmentgrooming'),
    path('update-appointmentgrooming-handler/<int:apptgrooming_id>', update_appointmentgrooming_handler, name='update_appointmentgrooming_handler'),
    path('delete-appointmentgrooming/<int:apptgrooming_id>', delete_appointmentgrooming, name='delete_appointmentgrooming'),
    path('finished-appointmentgrooming/<int:apptgrooming_id>', finished_appointmentgrooming, name='finished_appointmentgrooming'),
]