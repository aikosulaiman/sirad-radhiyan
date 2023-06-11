from django.db import models
from user.models import User, Dokter, Customer, Hewan
import uuid

STATUS_CHOICES = [
    ('Menunggu Konfirmasi', 'Menunggu Konfirmasi'),
    ('Disetujui', 'Disetujui'),
    ('Ditolak', 'Ditolak'),
    ('Dibatalkan', 'Dibatalkan'),
    ('Selesai', 'Selesai'),
]


class AppointmentDokter(models.Model):
    appointment_id = models.CharField(max_length=10, unique=True)
    dokter = models.ForeignKey(Dokter, on_delete=models.CASCADE)
    hewan = models.ForeignKey(Hewan, on_delete=models.CASCADE)
    pemilik = models.ForeignKey(Customer, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=40, blank=False, null=False, default='Menunggu Konfirmasi')
    keluhan = models.TextField(blank=True, null=True)
    alasan = models.CharField(max_length=500, null=True, default='')
    def save(self, *args, **kwargs):   
        # check if appointment_id has been set, otherwise generate it
        if not self.appointment_id:
            # get the last appointment with the APTDOC prefix
            last_appointment = AppointmentDokter.objects.filter(
                appointment_id__startswith='APTDOC').order_by('-appointment_id').first()

            # set the appointment_id to the next number in the sequence
            if last_appointment:
                last_number = int(last_appointment.appointment_id[6:])
                next_number = last_number + 1
            else:
                next_number = 1

            self.appointment_id = f'APTDOC{next_number:04d}'

        super().save(*args, **kwargs)