# Generated by Django 4.1.7 on 2023-03-18 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hewan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('jenis', models.CharField(max_length=100)),
                ('ras', models.CharField(max_length=100)),
                ('warna', models.CharField(max_length=100)),
                ('umur', models.CharField(max_length=100)),
                ('note', models.TextField(blank=True, null=True)),
                ('pemilik', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField()),
                ('hewan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sirad.hewan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]