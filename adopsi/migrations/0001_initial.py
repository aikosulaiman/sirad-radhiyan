# Generated by Django 4.1.7 on 2023-04-26 09:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Adopsi',
            fields=[
                ('hewan_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=1000)),
                ('jenis', models.CharField(max_length=1000)),
                ('ras', models.CharField(max_length=1000)),
                ('warna', models.CharField(max_length=1000)),
                ('deskripsi', models.CharField(max_length=1000)),
            ],
        ),
    ]
