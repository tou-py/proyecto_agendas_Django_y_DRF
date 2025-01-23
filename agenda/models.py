from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, nombres, apellidos, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico es obligatorio")
        email = self.normalize_email(email)
        user = self.model(
            email=email, nombres=nombres, apellidos=apellidos, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, nombres, apellidos, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, nombres, apellidos, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    nombres = models.CharField(max_length=255)
    apellidos = models.CharField(max_length=255)
    password_reset_token = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nombres", "apellidos"]

    objects = CustomUserManager()  # Asignar el UserManager personalizado

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Especialista(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    numero_telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.nombres} {self.user.apellidos}"


class Paciente(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    numero_telefono = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.nombres} {self.user.apellidos}"


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
        return f"Cita {self.id} - {self.paciente.user.nombres} {self.paciente.user.apellidos} con {self.especialista.user.nombres} {self.especialista.user.apellidos}"
