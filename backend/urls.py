from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView # Para Documentación

from savings.views.ml_views import PredictCategoryView # IA Categorización

urlpatterns = [
    # Documentación
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Endpoints web
    path('admin/', admin.site.urls),
    path('api/', include('savings.urls')),

    #Endpoints IA
    path("api/predict-category/", PredictCategoryView.as_view(), name="predict-category"),

]
