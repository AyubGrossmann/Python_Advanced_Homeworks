from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.core import mail
from .models import Task

User = get_user_model()

@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class TaskSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="signal_user", password="StrongPass123!",
            email="signal@example.com"
        )
        self.task = Task.objects.create(
            title="Тестовая задача", owner=self.user, status="New"
        )

    def test_email_when_status_changes(self):
        self.task.status = "In progress"
        self.task.save()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["signal@example.com"])

    def test_no_email_without_status_change(self):
        self.task.title = "Новое название"
        self.task.save()
        self.assertEqual(len(mail.outbox), 0)

    def test_no_email_on_task_creation(self):
        Task.objects.create(
            title="Другая задача", owner=self.user, status="New"
        )
        self.assertEqual(len(mail.outbox), 0)
