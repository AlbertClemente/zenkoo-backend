from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from savings.models import SavingGoal, User
from datetime import datetime

class SavingGoalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='ahorro@zenkoo.com',
            password='clave123',
            date_of_birth='1990-01-01'
        )
        self.client.force_authenticate(user=self.user)

        self.data = {
            'title': 'Meta nueva',
            'target_amount': '5000.00',
            'current_amount': '100.00',
            'deadline': datetime.now().isoformat(),
            'status': 'active'
        }

    def test_create_saving_goal(self):
        response = self.client.post(reverse('savinggoal-list-create'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_saving_goals(self):
        SavingGoal.objects.create(user=self.user, **self.data)
        response = self.client.get(reverse('savinggoal-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_saving_goal(self):
        goal = SavingGoal.objects.create(user=self.user, **self.data)
        response = self.client.patch(
            reverse('savinggoal-detail', args=[goal.id]),
            {'status': 'completed'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'completed')

    def test_delete_saving_goal(self):
        goal = SavingGoal.objects.create(user=self.user, **self.data)
        response = self.client.delete(reverse('savinggoal-detail', args=[goal.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authentication_required(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(reverse('savinggoal-list-create'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)