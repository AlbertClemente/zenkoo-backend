from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from savings.serializers import UserRegisterSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    post=extend_schema(
        tags=["Users"],
        summary="Registro de usuario",
        description="Permite registrar un nuevo usuario en la plataforma Zenkoo.",
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="Datos inválidos (email ya registrado)")
        },
    )
)
class UserRegisterView(APIView):
    """Permite a nuevos usuarios registrarse"""
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        tags=["Users"],
        summary="Obtener perfil",
        description="Devuelve los datos del usuario autenticado.",
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    put=extend_schema(
        tags=["Users"],
        summary="Actualizar perfil",
        description="Actualiza completamente el perfil del usuario.",
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    patch=extend_schema(
        tags=["Users"],
        summary="Actualizar parcialmente perfil",
        description="Actualiza algunos campos del perfil del usuario.",
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    delete=extend_schema(
        tags=["Users"],
        summary="Eliminar cuenta",
        description="Elimina al usuario autenticado de la plataforma.",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        request.user.delete()
        return Response({"detail": "Usuario eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)
