from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MonthlyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()  # Solo se usa año y mes
    reserved_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reflection = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'month']
