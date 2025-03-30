# Generated by Django 5.0.4 on 2025-03-30 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0007_rentalbooking_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('Showroom', 'Showroom'), ('Customer', 'Customer'), ('Dealer', 'Dealer')], max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('complaint_text', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Resolved', 'Resolved')], default='Pending', max_length=10)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
