import os

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


class HabitTestCase(APITestCase):
    def setUp(self):
        """
        Создает тестового пользователя и привычку для использования в других тестах.
        """
        self.user = User.objects.create(email="test@gmail.com")
        self.habit = Habit.objects.create(
            place="парк",
            time="08:00:00",
            action="приседания",
            is_nice_habit=False,
            frequency_number=1,
            frequency_unit="days",
            reward="съесть яблоко",
            duration="120",
            is_public=True,
            user=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        """
        Проверяет, что детали конкретной привычки доступны через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 200 OK
        - В ответе должна содержаться действительная информация о привычке
        """
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        """
        Проверяет, что новая привычка может быть успешно создана через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 201 Created
        - Количество записей в базе данных должно увеличиться на 1
        """
        url = reverse("habits:habits-list")
        data = {
            "place": "дом",
            "time": "20:40:00",
            "action": "протереть пыль",
            "is_pleasant": False,
            "frequency_number": 1,
            "frequency_unit": "days",
            "reward": "посмотреть фильм",
            "duration": "00:02:00",
            "is_public": True,
            "user": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_list(self):
        """
        Проверяет, что список всех привычек доступен через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 200 OK
        """
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_update(self):
        """
        Проверяет, что существующая привычка может быть успешно обновлена через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 200 OK
        - Обновленная информация должна соответствовать отправленным данным
        """
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        data = {
            "reward": "посмотреть фильм",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "посмотреть фильм")

    def test_public_habit_list(self):
        """
        Проверяет, что список публичных привычек доступен через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 200 OK
        """
        url = reverse("habits:public")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_delete(self):
        """
        Проверяет, что существующая привычка может быть успешно удалена через API.

        Ожидаемое поведение:
        - HTTP-код ответа должен быть 204 No Content
        - Количество записей в базе данных должно уменьшиться на 1
        """
        url = reverse("habits:habits-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)
