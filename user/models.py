import uuid
from django.db import models

# Create your models here.
ROLE_CHOICES = [
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
    ('Karyawan', 'Karyawan'),
    ('Dokter', 'Dokter'),
    ('Groomer', 'Groomer'),
]

JENIS_CHOICES = [
    ('Layanan', 'Layanan'),
    ('Produk', 'Produk'),
]

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(choices= ROLE_CHOICES, max_length=40)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    no_telepon = models.CharField(max_length=12)
    password = models.CharField(max_length=50)

class Customer(User):
    is_vip = models.BooleanField(default=False)
    
class Dokter(User):
    tarif = models.IntegerField()

class Hewan(models.Model):
    hewan_id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    jenis = models.CharField(max_length=50)
    umur = models.IntegerField()
    note = models.CharField(max_length=200)
    pemilik = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Produk(models.Model):
    id = models.AutoField(primary_key=True)
    nama = models.CharField(max_length=50)
    harga = models.CharField(max_length=50)
    status = models.BooleanField(default=False)
    jenis = models.CharField(choices= JENIS_CHOICES, max_length=40)