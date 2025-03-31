from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Expense
from savings.serializers import ExpenseSerializer

class ExpenseListCreateView(ListCreateAPIView):
    """Lista y crea gastos asociados al usuario autenticado"""
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)