from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Reflection
from savings.serializers import ReflectionSerializer

class ReflectionListCreateView(ListCreateAPIView):
    """Lista y crea reflexiones del usuario autenticado"""
    serializer_class = ReflectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reflection.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
