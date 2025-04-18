from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import SavingGoal
from savings.serializers import SavingGoalSerializer
from savings.pagination import SavingGoalsPagination
from django_filters.rest_framework import DjangoFilterBackend

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Saving Goals"],
        summary="Listar metas de ahorro",
        description="Devuelve todas las metas de ahorro del usuario autenticado.",
        responses={
            200: SavingGoalSerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Saving Goals"],
        summary="Crear una meta de ahorro",
        description="Permite crear una nueva meta de ahorro asociada al usuario autenticado.",
        responses={
            201: SavingGoalSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class SavingGoalListCreateView(ListCreateAPIView):
    """Lista y crea metas de ahorro del usuario autenticado"""
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend] # usar filtros
    filterset_fields = ['status']  # filtrar por campo status
    pagination_class = SavingGoalsPagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SavingGoal.objects.none()
        return SavingGoal.objects.filter(user=self.request.user).order_by('deadline')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        tags=["Saving Goals"],
        summary="Obtener meta de ahorro por ID",
        description="Devuelve los detalles de una meta si pertenece al usuario autenticado.",
        responses={
            200: SavingGoalSerializer,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    put=extend_schema(
        tags=["Saving Goals"],
        summary="Actualizar completamente una meta",
        description="Reemplaza por completo los datos de una meta.",
        responses={
            200: SavingGoalSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    patch=extend_schema(
        tags=["Saving Goals"],
        summary="Actualizar parcialmente una meta",
        description="Modifica algunos campos de una meta de ahorro.",
        responses={
            200: SavingGoalSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    delete=extend_schema(
        tags=["Saving Goals"],
        summary="Eliminar meta de ahorro",
        description="Elimina una meta si pertenece al usuario.",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    )
)
class SavingGoalDetailView(RetrieveUpdateDestroyAPIView):
    """Obtiene, actualiza o elimina una meta de ahorro concreta del usuario autenticado"""
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return SavingGoal.objects.none()
        return SavingGoal.objects.filter(user=self.request.user)
