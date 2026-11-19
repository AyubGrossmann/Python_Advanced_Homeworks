from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task

User = get_user_model()

class TaskOwnerTests(APITestCase):
    def setUp(self):
        self.user_one = User.objects.create_user(
            username="user_one", password="StrongPass123!"
        )
        self.user_two = User.objects.create_user(
            username="user_two", password="StrongPass123!"
        )
        self.task = Task.objects.create(
            title="Задача первого пользователя", owner=self.user_one
        )

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(user=self.user_two)
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], [])

    def test_owner_can_update_task(self):
        self.client.force_authenticate(user=self.user_one)
        response = self.client.patch(
            f"/api/tasks/{self.task.id}/",
            {"title": "Обновленная задача"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_user_cannot_open_foreign_task(self):
        self.client.force_authenticate(user=self.user_two)
        response = self.client.get(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
