from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class AuthTests(APITestCase):
    def setUp(self):
        self.first_name = 'Nuevo'
        self.last_name = 'User'
        self.email = 'user@zenkoo.com'
        self.password = 'clave123'
        self.date_of_birth = '1995-05-01'
        User = get_user_model()
        User.objects.create_user(email=self.email, password=self.password, date_of_birth=self.date_of_birth)

    def test_login_success(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'email': self.email,
            'password': self.password,

        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
