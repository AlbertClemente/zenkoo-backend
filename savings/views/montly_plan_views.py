from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from django.db.models import Sum
from savings.models import Income, Expense, MonthlyPlan, Reflection
from savings.serializers import MonthlyPlanSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from datetime import datetime

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

@extend_schema_view(
    get=extend_schema(
        tags=["MonthlyPlan"],
        summary="Resumen mensual (Kakeibo)",
        description="Devuelve los ingresos, gastos, ahorro real y ahorro reservado del mes actual, junto con la reflexión si existe.",
        responses={
            200: MonthlyPlanSerializer,
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

        # Ingresos y gastos del mes
        incomes = Income.objects.filter(user=user, created_at__year=month_start.year, created_at__month=month_start.month)
        expenses = Expense.objects.filter(user=user, created_at__year=month_start.year, created_at__month=month_start.month)

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        real_savings = total_income - total_expense

        # Plan mensual
        plan, _ = MonthlyPlan.objects.get_or_create(user=user, month=month_start)

        serializer = self.get_serializer(plan, context={
            'income': total_income,
            'expense': total_expense,
            'real_savings': real_savings
        })
        return Response(serializer.data)

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
class MonthlyPlanCreateUpdateView(generics.GenericAPIView):
    serializer_class = MonthlyPlanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        today = now().date()
        month_start = today.replace(day=1)

        data = request.data.copy()
        data['month'] = month_start

        # Obtener ingresos y gastos
        incomes = Income.objects.filter(user=user, created_at__year=month_start.year,
                                        created_at__month=month_start.month)
        expenses = Expense.objects.filter(user=user, created_at__year=month_start.year,
                                          created_at__month=month_start.month)

        total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        real_savings = total_income - total_expense

        # Obtener o crear el plan mensual
        plan, created = MonthlyPlan.objects.get_or_create(user=user, month=month_start)

        # Si el campo reflection_id está presente, actualizamos la reflexión
        reflection_pk = request.data.get('reflection_pk', None)

        if reflection_pk:
            try:
                reflection = Reflection.objects.get(id=reflection_pk)
                plan.reflection = reflection
                plan.save()
            except Reflection.DoesNotExist:
                return Response({"error": "Reflexión no encontrada"}, status=status.HTTP_400_BAD_REQUEST)

        # Guardar o actualizar el plan mensual
        serializer = self.get_serializer(plan, data=data, partial=True, context={
            'income': total_income,
            'expense': total_expense,
            'real_savings': real_savings
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        tags=["MonthlyPlan"],
        summary="Obtener plan mensual por ID",
        responses={200: MonthlyPlanSerializer}
    ),
    put=extend_schema(
        tags=["MonthlyPlan"],
        summary="Actualizar plan mensual por ID",
        request=MonthlyPlanSerializer,
        responses={200: MonthlyPlanSerializer}
    ),
)
class MonthlyPlanRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = MonthlyPlan.objects.all()
    serializer_class = MonthlyPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Asegura que el usuario solo accede a sus propios planes
        return MonthlyPlan.objects.filter(user=self.request.user)