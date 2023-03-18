from django.db import models
from django.contrib.auth.models import User


# class User(AbstractUser):
#     pass
#     id = models.UUIDField
#     nama = models.CharField(max_length=100)
#     role = models.CharField(max_length=100)
#     email = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return self.nama

class Hewan(models.Model):
    nama = models.CharField(max_length=100)
    jenis = models.CharField(max_length=100)
    ras = models.CharField(max_length=100)
    warna = models.CharField(max_length=100)
    umur = models.CharField(max_length=100)
    note = models.TextField(null=True, blank=True)
    pemilik = models.CharField(max_length=100)

    def __str__(self):
        return self.nama
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    body = models.TextField()

    def __str__(self):
        return self.body[0:50]