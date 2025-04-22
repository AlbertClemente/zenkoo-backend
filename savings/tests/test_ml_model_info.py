from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class ModelInfoTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='admin@zenkoo.com',
            password='admin123',
            is_staff=True,
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.admin)

    def test_model_info_contains_expected_keys(self):
        url = reverse('model-info')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('sampleCount', response.data)
        self.assertIn('accuracy', response.data)
        self.assertIn('lastTrainedAt', response.data)

