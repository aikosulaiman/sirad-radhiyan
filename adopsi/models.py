import uuid
from django.db import models

# Create your models here.
class Adopsi(models.Model):
    hewan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=1000)
    jenis = models.CharField(max_length=1000)
    ras = models.CharField(max_length=1000)
    warna = models.CharField(max_length=1000)
    deskripsi =  models.CharField(max_length=1000)