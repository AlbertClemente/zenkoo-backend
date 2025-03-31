from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from savings.models import Cripto
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

User = get_user_model()

class CriptoTests(APITestCase):

    def setUp(self):
        # Crear usuario y obtener token
        self.user = User.objects.create_user(
            email='usuario@correo.com',
            password='contrasenyaSuperFuerte123',
            date_of_birth=date(1990, 1, 1)
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.cripto_url = reverse('cripto-list')
        self.update_url = reverse('cripto-update')

    def test_get_criptos(self):
        Cripto.objects.create(name="Bitcoin", symbol="BTC", price=75000)
        Cripto.objects.create(name="Ethereum", symbol="ETH", price=1600)

        response = self.client.get(self.cripto_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['symbol'], "BTC")

    def test_post_actualizar_criptos(self):
        response = self.client.post(self.update_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Cripto.objects.filter(symbol="BTC").exists())
        self.assertTrue(Cripto.objects.filter(symbol="ETH").exists())
