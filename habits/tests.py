from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user1@example.com', password='StrongPass123')
        self.other_user = User.objects.create_user(email='user2@example.com', password='StrongPass123')
        self.client.force_authenticate(self.user)

    def test_create_habit_success(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Дом',
                'time': '08:30:00',
                'action': 'Зарядка',
                'is_pleasant': False,
                'periodicity': 1,
                'reward': 'Кофе',
                'execution_time': 60,
                'is_public': False,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)

    def test_cannot_set_related_and_reward_together(self):
        pleasant = Habit.objects.create(
            owner=self.user,
            place='Дом',
            time=time(10, 0),
            action='Выпить чай',
            is_pleasant=True,
            periodicity=1,
            execution_time=30,
        )

        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Офис',
                'time': '09:00:00',
                'action': 'Читать книгу',
                'is_pleasant': False,
                'related_habit': pleasant.id,
                'periodicity': 1,
                'reward': 'Сериал',
                'execution_time': 90,
                'is_public': False,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_execution_time_limit(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Парк',
                'time': '07:00:00',
                'action': 'Бег',
                'is_pleasant': False,
                'periodicity': 1,
                'reward': 'Смузи',
                'execution_time': 121,
                'is_public': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_limit(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Парк',
                'time': '07:00:00',
                'action': 'Бег',
                'is_pleasant': False,
                'periodicity': 8,
                'reward': 'Смузи',
                'execution_time': 100,
                'is_public': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_cannot_be_zero(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Парк',
                'time': '07:00:00',
                'action': 'Бег',
                'is_pleasant': False,
                'periodicity': 0,
                'reward': 'Смузи',
                'execution_time': 100,
                'is_public': True,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_habit_without_reward_and_related(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Дом',
                'time': '21:00:00',
                'action': 'Теплая ванна',
                'is_pleasant': True,
                'periodicity': 1,
                'reward': 'Шоколад',
                'execution_time': 90,
                'is_public': False,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_useful_habit_requires_reward_or_related(self):
        response = self.client.post(
            reverse('habit-list-create'),
            {
                'place': 'Дом',
                'time': '07:30:00',
                'action': 'Прогулка',
                'is_pleasant': False,
                'periodicity': 1,
                'execution_time': 60,
                'is_public': False,
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_only_own_habits(self):
        Habit.objects.create(
            owner=self.user,
            place='Дом',
            time=time(8, 0),
            action='Медитация',
            periodicity=1,
            reward='Чай',
            execution_time=60,
        )
        Habit.objects.create(
            owner=self.other_user,
            place='Дом',
            time=time(9, 0),
            action='Прогулка',
            periodicity=1,
            reward='Кино',
            execution_time=60,
        )

        response = self.client.get(reverse('habit-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_public_habits_list(self):
        self.client.force_authenticate(user=None)
        Habit.objects.create(
            owner=self.other_user,
            place='Улица',
            time=time(9, 0),
            action='Прогулка',
            periodicity=1,
            reward='Кофе',
            execution_time=60,
            is_public=True,
        )
        Habit.objects.create(
            owner=self.other_user,
            place='Дом',
            time=time(10, 0),
            action='Чтение',
            periodicity=1,
            reward='Десерт',
            execution_time=60,
            is_public=False,
        )

        response = self.client.get(reverse('public-habit-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
