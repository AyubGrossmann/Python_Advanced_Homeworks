# Generated for Homework 8
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Название категории")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, unique=True, verbose_name="Название задачи")),
                ("description", models.TextField(blank=True, verbose_name="Описание задачи")),
                ("status", models.CharField(choices=[("New", "New"), ("In progress", "In progress"), ("Pending", "Pending"), ("Blocked", "Blocked"), ("Done", "Done")], default="New", max_length=20, verbose_name="Статус")),
                ("deadline", models.DateTimeField(blank=True, null=True, verbose_name="Дедлайн")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("categories", models.ManyToManyField(blank=True, related_name="tasks", to="tasks.category", verbose_name="Категории")),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="SubTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Название подзадачи")),
                ("description", models.TextField(blank=True, verbose_name="Описание подзадачи")),
                ("status", models.CharField(choices=[("New", "New"), ("In progress", "In progress"), ("Pending", "Pending"), ("Blocked", "Blocked"), ("Done", "Done")], default="New", max_length=20, verbose_name="Статус")),
                ("deadline", models.DateTimeField(blank=True, null=True, verbose_name="Дедлайн")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("task", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="subtasks", to="tasks.task", verbose_name="Основная задача")),
            ],
            options={
                "verbose_name": "Подзадача",
                "verbose_name_plural": "Подзадачи",
                "ordering": ["-created_at"],
            },
        ),
    ]
