# Generated by Django 4.1.7 on 2023-04-11 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0017_alter_event_title_alter_register_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='general_location',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='register_event',
            name='id',
            field=models.CharField(default='aKcvVp', editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]