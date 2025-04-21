from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from savings.serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated
from savings.models import Category

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
        # Crear el serializador de registro de usuario con los datos recibidos
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            # Crear el usuario
            user = serializer.save()

            # Crear categorías predeterminadas para el nuevo usuario
            categories = ["Supervivencia", "Ocio y vicio", "Cultura", "Extras"]
            for category_name in categories:
                Category.objects.get_or_create(name=category_name, type="expense", user=user)

            # Retornar los datos del nuevo usuario
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si el serializador no es válido, retornar los errores
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
        summary="(NO RECOMENDADO) Actualizar perfil completamente",
        description="Actualiza todo el perfil del usuario. ⚠️ Se deben enviar todos los campos requeridos, incluyendo fecha de nacimiento y otros.",
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="Datos inválidos o campos faltantes"),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    patch=extend_schema(
        tags=["Users"],
        summary="Actualizar perfil",
        description="""
        Permite modificar uno o varios campos del perfil del usuario (como nombre, apellidos o email).
        
        Este método es recomendado para formularios parciales, como la configuración del perfil.
        """,
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

@extend_schema(
    tags=["Users"],
    summary="Cambiar contraseña",
    description="Permite al usuario autenticado cambiar su contraseña actual por una nueva.",
    request=ChangePasswordSerializer,
    responses={
        200: OpenApiResponse(description="Contraseña cambiada correctamente"),
        400: OpenApiResponse(description="Datos inválidos o contraseña actual incorrecta"),
        401: OpenApiResponse(description="No autenticado"),
    },
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
