from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from savings.models import Reflection, MonthlyPlan
from savings.serializers import ReflectionSerializer

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Reflections"],
        summary="Listar reflexiones",
        responses={
            200: ReflectionSerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Reflections"],
        summary="Crear una reflexión",
        responses={
            201: ReflectionSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class ReflectionListCreateView(ListCreateAPIView):
    """Lista y crea reflexiones del usuario autenticado"""
    serializer_class = ReflectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reflection.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # Verificar los datos que llegan
        print("Datos de la solicitud:", self.request.data)

        # Crear la reflexión
        reflection = serializer.save(user=self.request.user)

        # Obtener el 'monthly_plan_id' de la solicitud
        monthly_plan_id = self.request.data.get('monthly_plan_id', None)
        print(self.request.data)
        if monthly_plan_id:
            try:
                # Buscar el MonthlyPlan con el ID proporcionado
                monthly_plan = MonthlyPlan.objects.get(id=monthly_plan_id)
                print("Plan mensual encontrado:", monthly_plan)

                # Asociar la reflexión con el MonthlyPlan
                reflection.monthly_plan = monthly_plan
                reflection.save()

            except MonthlyPlan.DoesNotExist:
                raise serializers.ValidationError("El plan mensual proporcionado no existe.")

@extend_schema_view(
    get=extend_schema(
        tags=["Reflections"],
        summary="Obtener reflexión por ID",
        responses={
            200: ReflectionSerializer,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    put=extend_schema(
        tags=["Reflections"],
        summary="Actualizar completamente una reflexión",
        responses={
            200: ReflectionSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    patch=extend_schema(
        tags=["Reflections"],
        summary="Actualizar parcialmente una reflexión",
        responses={
            200: ReflectionSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    ),
    delete=extend_schema(
        tags=["Reflections"],
        summary="Eliminar reflexión",
        responses={
            204: None,
            401: OpenApiResponse(description="No autenticado"),
            403: OpenApiResponse(description="No autorizado"),
            404: OpenApiResponse(description="No encontrada")
        },
    )
)
class ReflectionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Recupera, actualiza o elimina una reflexión del usuario autenticado"""
    serializer_class = ReflectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Reflection.objects.none()
        return Reflection.objects.filter(user=self.request.user)
