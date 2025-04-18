from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Income
from savings.serializers import IncomeSerializer
from savings.pagination import IncomePagination
from django_filters.rest_framework import DjangoFilterBackend
from savings.filters.filters_incomes import IncomeFilter

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Incomes"],
        summary="Listar ingresos",
        responses={
            200: IncomeSerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Incomes"],
        summary="Crear un ingreso",
        responses={
            201: IncomeSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class IncomeListCreateView(ListCreateAPIView):
    """Lista y crea ingresos asociados al usuario autenticado"""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IncomeFilter
    pagination_class = IncomePagination

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        tags=["Incomes"],
        summary="Obtener ingreso por ID",
        responses={
            200: IncomeSerializer,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    ),
    put=extend_schema(
        tags=["Incomes"],
        summary="Actualizar ingreso completamente",
        responses={
            200: IncomeSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    ),
    patch=extend_schema(
        tags=["Incomes"],
        summary="Actualizar ingreso parcialmente",
        responses={
            200: IncomeSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    ),
    delete=extend_schema(
        tags=["Incomes"],
        summary="Eliminar ingreso",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    )
)
class IncomeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)

