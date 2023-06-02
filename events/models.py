from django.db import models
import uuid
from user.models import Customer
import shortuuid

JENIS_CHOICES = [
    ('Vaksinasi', 'Vaksinasi'),
    ('Sterilisasi', 'Sterilisasi'),
    ('Seminar/Webinar', 'Seminar/Webinar'),
    ('Promo/Sale', 'Promo/Sale'),
    ('Lomba', 'Lomba'),
    ('Bazaar', 'Bazaar'),
    ('Special Event', 'Special Event'),
]

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=25)
    jenis = models.CharField(choices=JENIS_CHOICES, max_length=50, blank=False, null=False, default='Special Event')
    general_location = models.CharField(max_length=20)
    specific_location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    isVIP = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)

class Register_Event(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True, default=shortuuid.uuid()[:6])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date = models.DateTimeField()
