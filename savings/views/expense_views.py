from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Expense
from savings.serializers import ExpenseSerializer
from savings.pagination import ExpensePagination
from django_filters.rest_framework import DjangoFilterBackend
from savings.filters.filters_expenses import ExpenseFilter

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Expenses"],
        summary="Listar gastos",
        description="Devuelve la lista de gastos del usuario autenticado.",
        responses={
            200: ExpenseSerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Expenses"],
        summary="Crear un nuevo gasto",
        description="Crea un nuevo gasto asociado al usuario autenticado.",
        responses={
            201: ExpenseSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class ExpenseListCreateView(ListCreateAPIView):
    """Lista y crea gastos asociados al usuario autenticado"""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ExpenseFilter
    pagination_class = ExpensePagination

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def get_serializer_context(self):
        return {'request': self.request}

    def post(self, request, *args, **kwargs):
        print("Payload recibido en /api/expenses/:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("🔴 Errores del serializer:", serializer.errors)
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema_view(
    get=extend_schema(
        tags=["Expenses"],
        summary="Obtener gasto por ID",
        description="Devuelve los detalles de un gasto si pertenece al usuario autenticado.",
        responses={
            200: ExpenseSerializer,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No tienes permiso para acceder a este gasto"),
            404: OpenApiResponse(description="Gasto no encontrado")
        },
    ),
    put=extend_schema(
        tags=["Expenses"],
        summary="Actualizar gasto completamente",
        description="Reemplaza completamente un gasto existente si pertenece al usuario autenticado.",
        responses={
            200: ExpenseSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    ),
    patch=extend_schema(
        tags=["Expenses"],
        summary="Actualizar gasto parcialmente",
        description="Actualiza campos específicos de un gasto existente.",
        responses={
            200: ExpenseSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    ),
    delete=extend_schema(
        tags=["Expenses"],
        summary="Eliminar gasto",
        description="Elimina un gasto por ID si pertenece al usuario autenticado.",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrado")
        },
    )
)
class ExpenseDetailView(RetrieveUpdateDestroyAPIView):
    """Obtiene, actualiza o elimina un gasto concreto del usuario autenticado"""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Expense.objects.none()
        return Expense.objects.filter(user=self.request.user)
