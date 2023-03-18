from django.contrib import admin

# Register your models here.
from .models import Hewan, Message

admin.site.register(Hewan)
admin.site.register(Message)