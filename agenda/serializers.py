from rest_framework import serializers
from .models import CustomUser, Especialista, Paciente, Cita


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "nombres", "apellidos"]
        extra_kwargs = {"password": {"write_only": True}}


class EspecialistaSerializer(serializers.ModelSerializer):
    nombres = serializers.CharField(source="user.nombres", read_only=True)
    apellidos = serializers.CharField(source="user.apellidos", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Especialista
        fields = [
            "id",
            "nombres",
            "apellidos",
            "email",
            "fecha_nacimiento",
            "numero_telefono",
        ]


class EspecialistaRegisterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Especialista
        fields = ["user", "fecha_nacimiento", "numero_telefono"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create_user(
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
    user = CustomUserSerializer()

    class Meta:
        model = Paciente
        fields = ["user", "fecha_nacimiento", "numero_telefono"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create_user(**user_data)
        paciente = Paciente.objects.create(user=user, **validated_data)
        return paciente
