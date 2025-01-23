# Generated by Django 5.1.5 on 2025-01-23 04:33

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
            name='Especialista',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField()),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('numero_telefono', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=255)),
                ('apellidos', models.CharField(max_length=255)),
                ('fecha_nacimiento', models.DateField()),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('numero_telefono', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('motivo', models.TextField(blank=True, null=True)),
                ('aparatos_utilizados', models.TextField(blank=True, null=True)),
                ('tratamiento_aplicado', models.TextField(blank=True, null=True)),
                ('fecha_inicio', models.DateTimeField(blank=True, null=True)),
                ('fecha_fin', models.DateTimeField(blank=True, null=True)),
                ('sesion_actual', models.IntegerField(blank=True, null=True)),
                ('siguiente_sesion', models.IntegerField(blank=True, null=True)),
                ('es_ultima_sesion', models.BooleanField(default=False)),
                ('tratamiento_culminado', models.BooleanField(default=False)),
                ('especialista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.especialista')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.paciente')),
            ],
        ),
    ]
