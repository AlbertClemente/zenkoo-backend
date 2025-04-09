from rest_framework.generics import ListCreateAPIView, UpdateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from savings.models import Notification
from savings.serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse

@extend_schema_view(
    get=extend_schema(
        tags=["Notifications"],
        summary="Listar notificaciones",
        description="Devuelve todas las notificaciones del usuario autenticado.",
        responses={
            200: NotificationSerializer(many=True),
            401: OpenApiResponse(description="No autenticado")
        },
    ),
    post=extend_schema(
        tags=["Notifications"],
        summary="Crear notificación",
        description="Permite crear una notificación dirigida al usuario autenticado.",
        responses={
            201: NotificationSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        },
    )
)
class NotificationListCreateView(ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(
    tags=["Notifications"],
    summary="Marcar notificación como leída",
    description="Marca una notificación como leída si pertenece al usuario autenticado.",
    responses={
        200: NotificationSerializer,
        401: OpenApiResponse(description="No autenticado"),
        403: OpenApiResponse(description="No autorizado"),
        404: OpenApiResponse(description="No encontrada")
    },
)
class NotificationMarkReadView(UpdateAPIView):
    """Marcar una notificación como leída"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        instance.is_read = True
        instance.save()
        return Response(self.get_serializer(instance).data)

@extend_schema(
    tags=["Notifications"],
    summary="Contar notificaciones no leídas",
    description="Devuelve el número de notificaciones no leídas del usuario autenticado.",
    responses={
        200: OpenApiResponse(description="Número de notificaciones no leídas"),
        401: OpenApiResponse(description="No autenticado")
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return Response({"unread_count": count})

@extend_schema(
    tags=["Notifications"],
    summary="Obtener o eliminar notificación",
    description="Devuelve el detalle de una notificación o la elimina si pertenece al usuario autenticado.",
    responses={
        200: NotificationSerializer,
        204: OpenApiResponse(description="Eliminada correctamente"),
        401: OpenApiResponse(description="No autenticado"),
        403: OpenApiResponse(description="No autorizado"),
        404: OpenApiResponse(description="No encontrada"),
    },
)
class NotificationRetrieveDeleteView(RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
