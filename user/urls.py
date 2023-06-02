from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='Index'),
    path('add-user', views.add_user, name='add_user'),
    path('list-user', views.list_user, name='list_user'),
    path('list-customer', views.list_customer, name='list_customer'),
    path('delete-user/<uuid:id>', views.delete_user),
    path('update-user/<uuid:user_id>', views.update_user, name='update_user'),
    path('customer-registration', views.customer_registration, name="customer_registration"),
    path('update-user-handler/<uuid:user_id>', views.update_user_handler, name='update_user_handler'),
    path('list-produk', views.list_produk, name='list_produk'),
    path('add-produk', views.add_produk, name='add_produk'),
    path('delete-produk/<int:id>', views.delete_produk),
    path('update-produk/<int:produk_id>', views.update_produk, name='update_produk'),
    path('update-produk-handler/<int:produk_id>', views.update_produk_handler, name='update_produk_handler'),
    path('customer-approval/<uuid:id>', views.customer_approval, name='customer_approval'),
]