# Generated by Django 5.0.6 on 2024-05-22 04:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_request', models.CharField(choices=[("Demande d'info", "Demande d'info"), ('Reclamation', 'Reclamation'), ('Reclamation anonyme', 'Reclamation anonyme')], max_length=50)),
                ('company_name', models.CharField(max_length=255)),
                ('industry', models.CharField(max_length=255)),
                ('full_name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('observations', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Marche',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100)),
                ('numero_ao', models.CharField(max_length=100)),
                ('designation', models.TextField()),
                ('ouverture_financiere', models.DateField()),
                ('montant_dhht', models.DecimalField(decimal_places=2, max_digits=10)),
                ('attributaire', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NewsletterSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TableData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100)),
                ('numero_ao', models.CharField(max_length=100)),
                ('designation', models.TextField()),
                ('date_lancement', models.DateField()),
                ('date_remise', models.DateField()),
                ('date_ouverture', models.DateField()),
                ('estimation_projet_dhht', models.FloatField()),
                ('seance_ouverture', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
            ],
        ),
        
    ]