from django.urls import path
from .views import update_profile

urlpatterns = [
    path('', update_profile, name='read_profile'),
    # path('edit', update_profile, name='update_profile'),
]