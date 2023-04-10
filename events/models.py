from django.db import models
import uuid
from django.contrib.auth import get_user_model


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    general_location = models.CharField(max_length=100)
    specific_location = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField()
    isVIP = models.BooleanField(default=False)
    # attendees = models.ManyToManyField(Customer)
