from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from savings.ml.info import get_model_info
from savings.ml.retrain import retrain_model_from_db, NotEnoughDataError
from rest_framework import status
from savings.models import Income, Expense, SavingGoal

# Documentación
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiResponse

@extend_schema(
    tags=["Admin"],
    summary="Información del modelo",
    responses={200: OpenApiTypes.OBJECT}
)
class ModelInfoView(APIView):
    permission_classes = [IsAdminUser]  # Solo accesible para admin

    def get(self, request):
        return Response(get_model_info())

@extend_schema(
    tags=["Admin"],
    summary="Reentrenar modelo desde base de datos",
    responses={
        200: OpenApiResponse(description="Reentrenado correctamente"),
        400: OpenApiResponse(description="No hay suficientes datos"),
        500: OpenApiResponse(description="Error interno")
    }
)
class RetrainModelView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = None

    def post(self, request):
        try:
            retrain_model_from_db()
            return Response({"detail": "Modelo reentrenado correctamente desde base de datos."}, status=status.HTTP_200_OK)
        except NotEnoughDataError as e:
            return Response(
                {"code": e.code, "detail": e.detail},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error interno al reentrenar el modelo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    tags=["Admin"],
    summary="Estadísticas básicas de la plataforma",
    responses={200: OpenApiTypes.OBJECT}
)
class PlatformStatsView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = None

    def get(self, request):
        User = get_user_model()

        total_users = User.objects.count()
        total_incomes = Income.objects.count()
        total_expenses = Expense.objects.count()
        total_goals = SavingGoal.objects.count()
        total_saved = SavingGoal.objects.aggregate(total=models.Sum("current_amount"))["total"] or 0

        return Response({
            "total_users": total_users,
            "total_incomes": total_incomes,
            "total_expenses": total_expenses,
            "total_goals": total_goals,
            "total_saved": total_saved,
        })
