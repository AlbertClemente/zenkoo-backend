from rest_framework.test import APITestCase
from django.urls import reverse
from django.utils.timezone import now
from rest_framework import status
from savings.models import MonthlyPlan, Reflection, User, Income, Expense
from datetime import datetime, timezone

class MonthlyPlanTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.url_create_update = reverse('monthly-plan-create-update')
        self.url_get_summary = reverse('monthly-plan-current')
        self.month_start = now().date().replace(day=1)

    def test_create_monthly_plan_with_reserved_savings(self):
        data = {'reserved_savings': '250.00'}
        response = self.client.post(self.url_create_update, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reserved_savings'], '250.00')

    def test_update_reserved_savings_on_existing_plan(self):
        MonthlyPlan.objects.create(user=self.user, month=self.month_start, reserved_savings='100.00')
        data = {'reserved_savings': '300.00'}
        response = self.client.post(self.url_create_update, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reserved_savings'], '300.00')

    def test_create_monthly_plan_with_reflection(self):
        reflection = Reflection.objects.create(
            user=self.user,
            title='Reflexión mensual',
            content='He aprendido a controlar mis gastos.'
        )
        data = {
            'reserved_savings': '150.00',
            'reflection_id': str(reflection.id)
        }
        response = self.client.post(self.url_create_update, data)
        self.assertIsNotNone(response.data['reflection'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reflection']['id'], str(reflection.id))

    def test_update_monthly_plan_to_remove_reflection(self):
        reflection = Reflection.objects.create(
            user=self.user,
            title='Reflexión',
            content='Contenido',
        )
        plan = MonthlyPlan.objects.create(
            user=self.user,
            month=self.month_start,
            reserved_savings=200,
            reflection=reflection
        )
        data = {
            'reserved_savings': '180.00',
            'reflection_id': None
        }
        response = self.client.post(self.url_create_update, data, format='json')
        self.assertIsNone(response.data["reflection"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['reserved_savings'], '180.00')
        self.assertEqual(response.data["reflection"], None)

    def test_get_monthly_summary(self):
        Income.objects.create(user=self.user, amount=1000, date=self.month_start)
        Income.objects.create(user=self.user, amount=500, date=self.month_start)
        Expense.objects.create(user=self.user, amount=300, date=self.month_start)
        Expense.objects.create(user=self.user, amount=200, date=self.month_start)
        MonthlyPlan.objects.create(user=self.user, month=self.month_start, reserved_savings=100)

        response = self.client.get(self.url_get_summary)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["income"], "1500.00")
        self.assertEqual(response.data["expense"], "500.00")
        self.assertEqual(response.data["real_savings"], "1000.00")
        self.assertEqual(response.data["reserved_savings"], "100.00")
        self.assertIn("reflection", response.data)
        self.assertEqual(response.data["month"], self.month_start.strftime('%Y-%m-%d'))

    def test_summary_creates_plan_if_not_exists(self):
        user2 = User.objects.create_user(email='nouserplan@example.com', password='123456', date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc))
        self.client.force_authenticate(user=user2)
        response = self.client.get(self.url_get_summary)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MonthlyPlan.objects.filter(user=user2, month=self.month_start).count(), 1)

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url_create_update, {'reserved_savings': '100.00'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)