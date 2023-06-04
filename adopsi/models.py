import uuid, shortuuid
from django.db import models

from user.models import Customer
from django.utils import timezone

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
    quantity = models.IntegerField(default=0)

class Register_Adopsi(models.Model):
    id = models.CharField(max_length=6, primary_key=True, editable=False, unique=True, default=shortuuid.uuid()[:6])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hewan = models.ForeignKey(Adopsi, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=50, blank=False, null=False, default='Menunggu konfirmasi')
    date_adopted = models.DateTimeField(default=timezone.now)
    alasan = models.TextField(default="")