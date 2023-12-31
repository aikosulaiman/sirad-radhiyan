# Generated by Django 4.1.7 on 2023-05-16 09:33

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=25)),
                ('general_location', models.CharField(max_length=20)),
                ('specific_location', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('description', models.TextField()),
                ('isVIP', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Register_Event',
            fields=[
                ('id', models.CharField(default='kiRvNc', editable=False, max_length=6, primary_key=True, serialize=False, unique=True)),
                ('date', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.event')),
            ],
        ),
    ]
