import uuid
from django.db import models
from django.conf import settings
from .category import Category

class Expense(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='expenses')

    def __str__(self):
        return f"{self.amount} € - {self.type} ({self.date.date()})"