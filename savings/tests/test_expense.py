from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import Expense, User, Category
from datetime import date

class ExpenseTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='gasto@zenkoo.com',
            password='clave123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(
            name='Transporte',
            type='expense',
            user=self.user
        )

        self.data = {
            'amount': '20.00',
            'date': date.today(),
            'type': 'Transporte diario',
            'category': self.category.id
        }

    def test_create_expense(self):
        response = self.client.post(reverse('expense-list-create'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_expense_list(self):
        data = self.data.copy()
        data['category'] = self.category  # 👈 usa instancia, no UUID
        Expense.objects.create(user=self.user, **data)
        response = self.client.get(reverse('expense-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('expense-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_expense(self):
        data = self.data.copy()
        data['category'] = self.category
        expense = Expense.objects.create(user=self.user, **data)
        new_data = {**self.data, 'type': 'Comida mensual'}
        response = self.client.put(reverse('expense-detail', args=[expense.id]), new_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], 'Comida mensual')

    def test_delete_expense(self):
        data = self.data.copy()
        data['category'] = self.category
        expense = Expense.objects.create(user=self.user, **data)
        response = self.client.delete(reverse('expense-detail', args=[expense.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)