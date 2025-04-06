from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Income, User
from datetime import date
from decimal import Decimal

class IncomeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='ingresos@zenkoo.com',
            password='claveingreso',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.data = {
            'amount': '1500.00',
            'date': date.today(),
            'type': 'Salario'
        }

    def test_create_income(self):
        response = self.client.post(reverse('income-list-create'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data['amount']), Decimal('1500.00'))

    def test_get_income_list(self):
        Income.objects.create(user=self.user, **self.data)
        response = self.client.get(reverse('income-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_income(self):
        income = Income.objects.create(user=self.user, **self.data)
        new_data = {**self.data, 'amount': '1800.00'}
        response = self.client.put(reverse('income-detail', args=[income.id]), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], '1800.00')

    def test_delete_income(self):
        income = Income.objects.create(user=self.user, **self.data)
        response = self.client.delete(reverse('income-detail', args=[income.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('income-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)