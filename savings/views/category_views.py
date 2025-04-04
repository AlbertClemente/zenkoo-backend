from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Category
from savings.serializers import CategorySerializer

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Categories"],
        summary="Listar categorías",
        responses={
            200: CategorySerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Categories"],
        summary="Crear una categoría",
        responses={
            201: CategorySerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class CategoryListCreateView(ListCreateAPIView):
    """Lista y crea categorías del usuario autenticado"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        tags=["Categories"],
        summary="Obtener categoría por ID",
        responses={
            200: CategorySerializer,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    put=extend_schema(
        tags=["Categories"],
        summary="Actualizar completamente una categoría",
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    patch=extend_schema(
        tags=["Categories"],
        summary="Actualizar parcialmente una categoría",
        responses={
            200: CategorySerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    delete=extend_schema(
        tags=["Categories"],
        summary="Eliminar categoría",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    )
)
class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Recupera, actualiza o elimina una categoría del usuario autenticado"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
