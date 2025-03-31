from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now
from savings.models import Expense, User, Category
from datetime import timedelta

class ExpenseTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='usuario@correo.com',
            password='superPassword123',
            first_name='Usuario',
            last_name='Ejemplo',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(
            name="Transporte", type="expense", user=self.user
        )
        self.expense_data = {
            'amount': 50.00,
            'date': (now() - timedelta(days=1)).isoformat(),
            'type': 'Taxi',
            'category': str(self.category.id)
        }
        self.url = reverse('expense-list-create')

    def test_create_expense(self):
        response = self.client.post(self.url, self.expense_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 1)
        self.assertEqual(response.data['amount'], '50.00')

    def test_get_expense_list(self):
        Expense.objects.create(
            user=self.user,
            amount=self.expense_data['amount'],
            date=self.expense_data['date'],
            type=self.expense_data['type'],
            category=self.category
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
