from django.urls import path
from .views import login, home, logout

app_name = 'loginlogout'

urlpatterns = [
 path('', home, name='home'),
 path('login', login, name='login'),
 path('logout',logout,name ="logout")
]