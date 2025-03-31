from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now, timedelta
from savings.models import SavingGoal, User

class SavingGoalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='ahorro@correo.com',
            password='segura123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)
        self.goal_data = {
            'target_amount': '1000.00',
            'deadline': now() + timedelta(days=30),
            'status': 'active'
        }

    def test_create_saving_goal(self):
        response = self.client.post(reverse('savinggoal-list-create'), self.goal_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_saving_goal_list(self):
        SavingGoal.objects.create(user=self.user, **self.goal_data)
        response = self.client.get(reverse('savinggoal-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
