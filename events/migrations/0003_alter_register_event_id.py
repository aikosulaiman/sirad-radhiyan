# Generated by Django 4.1.7 on 2023-05-16 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_register_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_event',
            name='id',
            field=models.CharField(default='G4hPgi', editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]
