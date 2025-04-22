from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import User, Category

class RegisterTests(APITestCase):
    def test_user_register_and_default_categories(self):
        url = reverse('user-register')
        payload = {
            'email': 'nuevo@zenkoo.com',
            'password': 'clave123',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'date_of_birth': '1995-05-01'
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email='nuevo@zenkoo.com').count(), 1)

        user = User.objects.get(email='nuevo@zenkoo.com')
        categories = Category.objects.filter(user=user)
        self.assertGreaterEqual(categories.count(), 4)  # Supervivencia, Ocio, Cultura, Extras
