# Generated by Django 4.1.7 on 2023-05-20 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_register_event_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='jenis',
            field=models.CharField(choices=[('Vaksinasi', 'Vaksinasi'), ('Sterilisasi', 'Sterilisasi'), ('Seminar/Webinar', 'Seminar/Webinar'), ('Promo/Sale', 'Promo/Sale'), ('Lomba', 'Lomba'), ('Bazaar', 'Bazaar'), ('Special Event', 'Special Event')], default='Special Event', max_length=50),
        ),
        migrations.AlterField(
            model_name='register_event',
            name='id',
            field=models.CharField(default='GvtPJq', editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]
