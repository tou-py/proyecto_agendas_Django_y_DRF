import logging
from django.core.cache import cache
from rest_framework import viewsets, status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
from .models import Especialista, Paciente, Cita
from .serializers import (
    EspecialistaSerializer,
    PacienteSerializer,
    CitaSerializer,
    CustomUserSerializer,
    PacienteRegisterSerializer,
    EspecialistaRegisterSerializer,
)
from twilio.rest import Client

User = get_user_model()  # Obtener el modelo de usuario personalizado

logger = logging.getLogger("citas")  # Obtener el logger de la aplicación


# Función para enviar mensajes de WhatsApp
# Crear una cuenta en Twilio y obtener el account_sid y auth_token
def enviar_whatsapp(mensaje, numero):
    account_sid = "tu_account_sid"
    auth_token = "tu_auth_token"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=mensaje,
        from_="whatsapp:+14155238886",  # Número de Twilio
        to=f"whatsapp:{numero}",
    )
    return message.sid


class EspecialistaViewSet(viewsets.ModelViewSet):
    queryset = Especialista.objects.all()
    serializer_class = EspecialistaSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Especialista creado: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error al crear especialista: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class EspecialistaRegisterView(generics.CreateAPIView):
    serializer_class = EspecialistaRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AprobarEspecialistaView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EspecialistaSerializer

    def post(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response(
                {"message": "Cuenta de especialista aprobada"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Paciente creado: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error al crear paciente: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PacienteRegisterView(generics.CreateAPIView):
    serializer_class = PacienteRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # Modifica solo el usuario autenticado


class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAdminUser]


class CitaPagination(PageNumberPagination):
    page_size = 5  # Elementos por página
    page_size_query_param = "page_size"  # Parámetro para cambiar el tamaño de la página
    max_page_size = 100  # Tamaño máximo de la página


class CitaViewSet(viewsets.ModelViewSet):
    queryset = Cita.objects.all()
    serializer_class = CitaSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CitaPagination  # Usar la paginación personalizada

    def get_queryset(self):
        cache_key = "citas_list"
        citas = cache.get(cache_key)
        if not citas:
            citas = Cita.objects.all()
            cache.set(cache_key, citas, timeout=60 * 15)  # Cachear por 15 minutos
        return citas

    def perform_create(self, serializer):
        cache_key = "citas_list"
        cache.delete(cache_key)  # Invalidar el caché
        serializer.save(especialista=self.request.user.especialista)
        cita = serializer.save()
        paciente = cita.paciente.user
        subject = "Cita Agendada"
        message = f"Hola {paciente.nombres}, tu cita ha sido agendada para el {cita.fecha_hora}."

        # Enviar correo electrónico
        send_mail(subject, message, "noreply@tudominio.com", [paciente.email])

        # Enviar WhatsApp
        enviar_whatsapp(message, paciente.numero_telefono)

    def perform_update(self, serializer):
        cache_key = "citas_list"
        cache.delete(cache_key)  # Invalidar el caché
        serializer.save()

    def perform_destroy(self, instance):
        cache_key = "citas_list"
        cache.delete(cache_key)  # Invalidar el caché
        instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            logger.info(f"Cita creada: {response.data}")
            return response
        except Exception as e:
            logger.error(f"Error al crear cita: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# vistas para recuperacion de contraseña
class PasswordResetRequestView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            token = get_random_string(50)  # Genera un token único
            user.password_reset_token = token
            user.save()
            # aqui tengo que recordar de colocar el dominio correcto
            reset_url = (
                f"http://dominio.com{reverse('password-reset-confirm')}?token={token}"
            )
            subject = "Restablecer contraseña"
            message = f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}"
            # Aqui debo recordar poner el correo correcto
            send_mail(subject, message, "correodereset@gmail.com", [user.email])

            return Response(
                {"message": "Se ha enviado un correo para restablecer la contraseña."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )


class PasswordResetConfirmView(APIView):
    def post(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        try:
            user = User.objects.get(password_reset_token=token)
            user.set_password(new_password)
            user.password_reset_token = None  # Elimina el token después de usarlo
            user.save()
            return Response(
                {"message": "Contraseña restablecida correctamente."},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST
            )


# vista para envio de notificaciones por whatsapp
