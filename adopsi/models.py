import uuid
from django.db import models

from user.models import Customer

STATUS_CHOICES = [
    ('Belum diadopsi', 'Belum diadopsi'),
    ('Diadopsi', 'Diadopsi'),
]
class Adopsi(models.Model):
    hewan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nama = models.CharField(max_length=1000)
    jenis = models.CharField(max_length=1000)
    ras = models.CharField(max_length=1000)
    warna = models.CharField(max_length=1000)
    deskripsi =  models.CharField(max_length=1000)
    # status =  models.CharField(max_length=50, default="Belum diadopsi")
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, blank=False, null=False, default='Belum diadopsi')