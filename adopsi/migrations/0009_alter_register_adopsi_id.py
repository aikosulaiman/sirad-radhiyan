# Generated by Django 4.1.7 on 2023-05-30 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adopsi', '0008_alter_register_adopsi_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register_adopsi',
            name='id',
            field=models.CharField(default='MXdbCJ', editable=False, max_length=6, primary_key=True, serialize=False, unique=True),
        ),
    ]
