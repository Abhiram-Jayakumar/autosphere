# Generated by Django 5.1.6 on 2025-03-05 05:58

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dealer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, unique=True)),
                ('registered_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('approval_status', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=128)),
                ('id_proof_number', models.CharField(max_length=50, unique=True)),
                ('profile_image_dealer', models.ImageField(blank=True, null=True, upload_to='profile_images_dealer/')),
                ('address', models.TextField()),
            ],
        ),
    ]
