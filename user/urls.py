from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('add-user', views.add_user, name='add_user'),
    path('list-user', views.list_user, name='list_user'),
    path('update-user/<uuid:user_id>', views.update_user, name='update_user'),
    path('update-user-handler/<uuid:user_id>', views.update_user_handler, name='update_user_handler')
]