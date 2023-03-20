from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('add-user', views.add_user, name='add_user'),
    path('list-user', views.list_user, name='list_user'),
    path('delete-user/<uuid:id>', views.delete_user),
]