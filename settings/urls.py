from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from agenda.views import (
    EspecialistaViewSet,
    PacienteViewSet,
    CitaViewSet,
    PacienteRegisterView,
    EspecialistaRegisterView,
    AprobarEspecialistaView,
    UpdateUserView,
    DeleteUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

# Rutas para Docs
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"especialistas", EspecialistaViewSet)
router.register(r"pacientes", PacienteViewSet)
router.register(r"citas", CitaViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path(
        "api/register/paciente/",
        PacienteRegisterView.as_view(),
        name="paciente-register",
    ),
    path(
        "api/register/especialista/",
        EspecialistaRegisterView.as_view(),
        name="especialista-register",
    ),
    path(
        "api/aprobar/especialista/<int:user_id>/",
        AprobarEspecialistaView.as_view(),
        name="aprobar-especialista",
    ),
    path("api/update-user/", UpdateUserView.as_view(), name="update-user"),
    path("api/delete-user/<int:pk>/", DeleteUserView.as_view(), name="delete-user"),
    # rutas para autenticación
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # rutas para recuperar contraseña
    path(
        "api/password-reset/", PasswordResetRequestView.as_view(), name="password-reset"
    ),
    path(
        "api/password-reset-confirm/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # Rutas para Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
