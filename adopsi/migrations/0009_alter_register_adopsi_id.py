# Generated by Django 4.1.7 on 2023-06-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("adopsi", "0008_alter_register_adopsi_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="register_adopsi",
            name="id",
            field=models.CharField(
                default="6bQk9M",
                editable=False,
                max_length=6,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
