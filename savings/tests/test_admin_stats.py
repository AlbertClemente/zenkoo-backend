from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class AdminStatsTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='admin@zenkoo.com',
            password='admin123',
            is_staff=True,
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.admin)

    def test_get_admin_stats(self):
        url = reverse('platform-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)
        self.assertIn('total_expenses', response.data)

    def test_get_model_info(self):
        url = reverse('model-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sampleCount', response.data)
        self.assertIn('accuracy', response.data)