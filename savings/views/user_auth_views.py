from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny

# Documentación
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Users"],
    summary="Iniciar sesión",
    description="Devuelve access y refresh tokens si las credenciales son válidas.",
    responses={200: OpenApiTypes.OBJECT}
)
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]

@extend_schema(
    tags=["Users"],
    summary="Refrescar token",
    description="Devuelve un nuevo token de acceso usando un refresh token válido.",
    responses={200: OpenApiTypes.OBJECT}
)
class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]
