import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Income(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')

    def __str__(self):
        return f"{self.amount} € - {self.type} ({self.date})"