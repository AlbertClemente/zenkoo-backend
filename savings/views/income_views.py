from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Income
from savings.serializers import IncomeSerializer

class IncomeListCreateView(ListCreateAPIView):
    """Lista y crea ingresos asociados al usuario autenticado"""
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)