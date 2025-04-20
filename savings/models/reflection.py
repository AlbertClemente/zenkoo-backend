import uuid
from django.db import models
from django.conf import settings

class Reflection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reflections')
    monthly_plan = models.OneToOneField('MonthlyPlan', on_delete=models.CASCADE, related_name='reflection_monthly_plan', null=True, blank=True)

    def __str__(self):
        return f"Reflexión de {self.user.email} el {self.created_at.date()}"
