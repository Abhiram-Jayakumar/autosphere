# Generated by Django 5.0.4 on 2025-03-29 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0006_testdrivebooking_dealer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalbooking',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
    ]
