from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..ml.predict import predict_category # Llamamos al script de predicción

# Documentación
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiResponse

class PredictCategoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["AI"],
        summary="Predecir categoría para un gasto o ingreso",
        description="Devuelve la categoría Kakeibo sugerida en base al campo tipo o descripción.",
        request={"type": "object", "properties": {"text": {"type": "string"}}},
        responses={
            200: {"type": "object", "properties": {"category": {"type": "string"}}},
            400: {"description": "Texto no proporcionado"},
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
        text = request.data.get("text", "")
        if not text:
            return Response({"error": "Texto no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = predict_category(text)
            return Response({"category": category})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
