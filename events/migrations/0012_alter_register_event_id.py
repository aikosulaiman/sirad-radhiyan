# Generated by Django 4.1.7 on 2023-04-11 05:28

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_register_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_event',
            name='id',
            field=models.UUIDField(default=shortuuid.main.ShortUUID.uuid, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]