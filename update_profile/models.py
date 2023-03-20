from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    email = models.CharField(max_length=1000000)

def __str__(self):
    return str(self.name)

class Hewan(models.Model):
    owner = models.ForeignKey(Profile, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    number = models.CharField(max_length=100)
    year = models.DateField(max_length=100)
    month = models.DateField(max_length=100)
    info = models.CharField(max_length=1000000)

    def __str__(self):
        return str(self.owner.name) + " " + str(self.name)