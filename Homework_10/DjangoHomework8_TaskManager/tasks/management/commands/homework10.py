from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tasks.models import Task, SubTask


class Command(BaseCommand):
    help = "Выполняет все ORM-запросы из домашнего задания 10"

    def handle(self, *args, **options):
        # Удаляем старую учебную задачу, если команда запускается повторно.
        # Подзадачи удалятся автоматически благодаря on_delete=models.CASCADE.
        Task.objects.filter(title="Prepare presentation").delete()

        self.stdout.write(self.style.MIGRATE_HEADING("1. СОЗДАНИЕ ЗАПИСЕЙ"))

        now = timezone.now()

        # Создаём основную задачу.
        task = Task.objects.create(
            title="Prepare presentation",
            description="Prepare materials and slides for the presentation.",
            status="New",
            deadline=now + timedelta(days=3),
        )
        self.stdout.write(f"Создана задача: {task}")

        # Создаём две подзадачи для основной задачи.
        subtask1 = SubTask.objects.create(
            title="Gather information",
            description="Find necessary information for the presentation.",
            status="New",
            deadline=now + timedelta(days=2),
            task=task,
        )

        subtask2 = SubTask.objects.create(
            title="Create slides",
            description="Create presentation slides.",
            status="New",
            deadline=now + timedelta(days=1),
            task=task,
        )

        self.stdout.write(f"Создана подзадача: {subtask1}")
        self.stdout.write(f"Создана подзадача: {subtask2}")

        self.stdout.write(self.style.MIGRATE_HEADING("2. ЧТЕНИЕ ЗАПИСЕЙ"))

        # Получаем все задачи со статусом New.
        new_tasks = Task.objects.filter(status="New")
        self.stdout.write("Задачи со статусом New:")
        if new_tasks.exists():
            for item in new_tasks:
                self.stdout.write(f"- {item.title}")
        else:
            self.stdout.write("Таких задач нет.")

        # Получаем подзадачи со статусом Done, у которых дедлайн уже прошёл.
        overdue_done_subtasks = SubTask.objects.filter(
            status="Done",
            deadline__lt=timezone.now(),
        )
        self.stdout.write("Просроченные подзадачи со статусом Done:")
        if overdue_done_subtasks.exists():
            for item in overdue_done_subtasks:
                self.stdout.write(f"- {item.title}")
        else:
            self.stdout.write(
                "Таких подзадач нет (созданные выше подзадачи имеют статус New)."
            )

        self.stdout.write(self.style.MIGRATE_HEADING("3. ИЗМЕНЕНИЕ ЗАПИСЕЙ"))

        # Меняем статус основной задачи.
        Task.objects.filter(title="Prepare presentation").update(
            status="In progress"
        )
        self.stdout.write("Статус Prepare presentation изменён на In progress.")

        # Переносим дедлайн первой подзадачи на два дня назад.
        SubTask.objects.filter(title="Gather information").update(
            deadline=timezone.now() - timedelta(days=2)
        )
        self.stdout.write("Дедлайн Gather information перенесён на два дня назад.")

        # Меняем описание второй подзадачи.
        SubTask.objects.filter(title="Create slides").update(
            description="Create and format presentation slides."
        )
        self.stdout.write("Описание Create slides изменено.")

        # Проверяем изменения и выводим обновлённые значения.
        task.refresh_from_db()
        subtask1.refresh_from_db()
        subtask2.refresh_from_db()

        self.stdout.write(f"Проверка Task.status: {task.status}")
        self.stdout.write(
            "Проверка Gather information deadline: "
            f"{timezone.localtime(subtask1.deadline).strftime('%d.%m.%Y %H:%M')}"
        )
        self.stdout.write(f"Проверка Create slides description: {subtask2.description}")

        self.stdout.write(self.style.MIGRATE_HEADING("4. УДАЛЕНИЕ ЗАПИСЕЙ"))

        # Удаляем основную задачу. Все её подзадачи удаляются каскадно.
        task_title = task.title
        task.delete()

        self.stdout.write(f"Задача '{task_title}' удалена.")
        remaining_subtasks = SubTask.objects.filter(
            title__in=["Gather information", "Create slides"]
        ).count()
        self.stdout.write(
            f"Количество оставшихся подзадач этой работы: {remaining_subtasks}"
        )

        self.stdout.write(self.style.SUCCESS(
            "Все операции ORM из домашнего задания 10 выполнены!"
        ))
