from savings.serializers import PredictCategoryInputSerializer
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from ..ml.predict import predict_category

class PredictCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PredictCategoryInputSerializer

    @extend_schema(
        tags=["AI"],
        summary="Predecir categoría para un gasto o ingreso",
        description="Devuelve la categoría Kakeibo sugerida en base al campo tipo o descripción.",
        request=PredictCategoryInputSerializer,
        responses={
            200: OpenApiResponse(description="Categoría predicha"),
            400: OpenApiResponse(description="Texto no proporcionado"),
        },
        examples=[
            OpenApiExample(
                "Ejemplo válido",
                value={"text": "Cena en restaurante"},
                response_only=False,
            )
        ]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        text = serializer.validated_data['text']
        try:
            category = predict_category(text)
            return Response({"category": category})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)