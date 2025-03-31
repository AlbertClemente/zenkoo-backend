from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from savings.models import Income
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
import uuid
from datetime import date

User = get_user_model()

class IncomeTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='usuario@correo.com',
            password='contrasenyaSuperFuerte123',
            date_of_birth=date(1990, 1, 1)
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.income_url = reverse('income-list-create')

        self.income = Income.objects.create(
            id=uuid.uuid4(),
            amount=1000,
            date=timezone.now(),
            type="Salario",
            user=self.user
        )

    def test_get_income_list(self):
        response = self.client.get(self.income_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['amount'], "1000.00")

    def test_create_income(self):
        data = {
            "amount": "1500.00",
            "date": timezone.now().isoformat(),
            "type": "Freelance"
        }
        response = self.client.post(self.income_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 2)

    def test_update_income(self):
        url = reverse('income-detail', args=[str(self.income.id)])
        data = {
            "amount": "2000.00",
            "date": self.income.date.isoformat(),
            "type": "Salario actualizado"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.income.refresh_from_db()
        self.assertEqual(str(self.income.amount), "2000.00")

    def test_delete_income(self):
        url = reverse('income-detail', args=[str(self.income.id)])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Income.objects.filter(id=self.income.id).exists())
