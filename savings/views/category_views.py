from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from savings.models import Category
from savings.serializers import CategorySerializer

class CategoryListCreateView(ListCreateAPIView):
    """Lista y crea categorías del usuario autenticado"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
