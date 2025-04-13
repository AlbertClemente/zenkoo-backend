from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from savings.ml.info import get_model_info
from savings.ml.retrain import retrain_model_from_db, NotEnoughDataError
from rest_framework import status

class ModelInfoView(APIView):
    permission_classes = [IsAdminUser]  # Solo accesible para admin

    def get(self, request):
        return Response(get_model_info())

class RetrainModelView(APIView):
    permission_classes = [IsAdminUser]

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