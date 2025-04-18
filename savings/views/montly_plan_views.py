from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Sum
from savings.models import Income, Expense, MonthlyPlan
from savings.serializers import MonthlyPlanSerializer
from datetime import datetime

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

@extend_schema_view(
    get=extend_schema(
        tags=["MonthlyPlan"],
        summary="Resumen mensual (Kakeibo)",
        description="Devuelve los ingresos, gastos, ahorro real y ahorro reservado del mes actual, junto con la reflexión si existe.",
        responses={
            200: OpenApiResponse(
                description="Resumen mensual",
                examples=[
                    OpenApiExample(
                        "Ejemplo de respuesta",
                        value={
                            "month": "2025-04",
                            "income": 2300.00,
                            "expense": 1950.00,
                            "real_savings": 350.00,
                            "reserved_savings": 200.00,
                            "reflection": "Este mes he gastado mucho en comida fuera de casa."
                        }
                    )
                ]
            ),
            401: OpenApiResponse(description="No autenticado")
        }
    )
)
class MonthlyPlanCurrentView(generics.GenericAPIView):
    serializer_class = MonthlyPlanSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = now().date()
        month_start = today.replace(day=1)
        month_str = month_start.strftime('%Y-%m')  # para comparar fácilmente

        incomes = Income.objects.filter(user=user, created_at__year=month_start.year, created_at__month=month_start.month)
        expenses = Expense.objects.filter(user=user, created_at__year=month_start.year, created_at__month=month_start.month)

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        real_savings = total_income - total_expense

        plan, _ = MonthlyPlan.objects.get_or_create(user=user, month=month_start)

        return Response({
            'month': month_str,
            'income': total_income,
            'expense': total_expense,
            'real_savings': real_savings,
            'reserved_savings': plan.reserved_savings,
            'reflection': plan.reflection,
        })

@extend_schema_view(
    post=extend_schema(
        tags=["MonthlyPlan"],
        summary="Crear o actualizar plan mensual",
        description="Permite guardar la meta de ahorro (reserved_savings) y una reflexión mensual (reflection).",
        request=MonthlyPlanSerializer,
        responses={
            200: MonthlyPlanSerializer,
            400: OpenApiResponse(description="Datos inválidos"),
            401: OpenApiResponse(description="No autenticado")
        }
    )
)
class MonthlyPlanCreateUpdateView(generics.CreateAPIView):
    serializer_class = MonthlyPlanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = now().date()
        month_start = today.replace(day=1)
        data = request.data.copy()
        data['month'] = month_start

        plan, created = MonthlyPlan.objects.get_or_create(user=user, month=month_start)
        serializer = self.get_serializer(plan, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)