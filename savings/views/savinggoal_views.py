from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import SavingGoal
from savings.serializers import SavingGoalSerializer

class SavingGoalListCreateView(ListCreateAPIView):
    """Lista y crea metas de ahorro del usuario autenticado"""
    serializer_class = SavingGoalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavingGoal.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
