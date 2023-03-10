from django.urls import path
from loginlogout.views import *

urlpatterns = [
    path('', index, name='Index'),
]