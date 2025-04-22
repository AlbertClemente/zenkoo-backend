from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from unittest.mock import patch

class RetrainModelTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_user(
            email='admin@zenkoo.com',
            password='admin123',
            is_staff=True,
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.admin)

    @patch('savings.views.admin.retrain_model_from_db')
    def test_retrain_success(self, mock_retrain):
        mock_retrain.return_value = None
        url = reverse('retrain-model')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Modelo reentrenado correctamente', response.data['detail'])
