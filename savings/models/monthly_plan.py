import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from .reflection import Reflection

User = get_user_model()

class MonthlyPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.DateField()  # Solo se usa año y mes
    reserved_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reflection = models.OneToOneField(Reflection, on_delete=models.CASCADE, null=True, blank=True, related_name='monthly_plan_reflection')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='monthly_plans')

    class Meta:
        unique_together = ['user', 'month']