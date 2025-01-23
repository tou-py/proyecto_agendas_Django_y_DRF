from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Especialista, Paciente, Cita


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}


class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = [
            "id",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "correo_electronico",
            "numero_telefono",
        ]


class EspecialistaRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Especialista
        fields = [
            "user",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "correo_electronico",
            "numero_telefono",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(
            **user_data, is_active=False
        )  # Cuenta inactiva hasta aprobación
        especialista = Especialista.objects.create(user=user, **validated_data)
        return especialista


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        fields = "__all__"


class CitaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = "__all__"

    def validate(self, data):
        if data["fecha_inicio"] > data["fecha_fin"]:
            raise serializers.ValidationError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return data


class PacienteRegisterSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Paciente
        fields = [
            "user",
            "nombres",
            "apellidos",
            "fecha_nacimiento",
            "correo_electronico",
            "numero_telefono",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        paciente = Paciente.objects.create(user=user, **validated_data)
        return paciente
