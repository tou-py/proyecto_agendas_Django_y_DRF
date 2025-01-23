from django.db import models
from django.contrib.auth.models import User


class Especialista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField()
    numero_telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre_completo


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField()
    correo_electronico = models.EmailField()
    numero_telefono = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre_completo


class Cita(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField()
    motivo = models.TextField(blank=True, null=True)
    aparatos_utilizados = models.TextField(blank=True, null=True)
    tratamiento_aplicado = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=True, null=True)
    fecha_fin = models.DateTimeField(blank=True, null=True)
    sesion_actual = models.IntegerField(blank=True, null=True)
    siguiente_sesion = models.IntegerField(blank=True, null=True)
    es_ultima_sesion = models.BooleanField(default=False)
    tratamiento_culminado = models.BooleanField(default=False)

    def __str__(self):
        return f"Cita {self.id} - {self.paciente.nombre_completo} con {self.especialista.nombre_completo}"
