from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('add-user', views.add_user, name='add_user'),
    path('list-user', views.list_user, name='list_user'),
    path('delete-user/<uuid:id>', views.delete_user),
    path('update-user/<uuid:user_id>', views.update_user, name='update_user'),
    path('customer-registration/', views.customer_registration, name="customer_registration"),
    path('update-user-handler/<uuid:user_id>', views.update_user_handler, name='update_user_handler'),
    path('list-produk', views.list_produk, name='list_produk'),
]