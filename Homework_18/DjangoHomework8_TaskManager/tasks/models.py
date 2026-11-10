from django.db import models
from django.utils import timezone


class ActiveCategoryManager(models.Manager):
    # По умолчанию показываем только категории, которые не удалены.
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название категории",
    )
    is_deleted = models.BooleanField(default=False, verbose_name="Удалена")
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата удаления",
    )

    objects = ActiveCategoryManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        # Мягкое удаление: запись остаётся в базе.
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at"])
        return (1, {self._meta.label: 1})


class Task(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("In progress", "In progress"),
        ("Pending", "Pending"),
        ("Blocked", "Blocked"),
        ("Done", "Done"),
    ]

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название задачи",
    )
    description = models.TextField(blank=True, verbose_name="Описание задачи")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Статус",
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дедлайн",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="tasks",
        verbose_name="Категории",
    )

    class Meta:
        db_table = "task_manager_task"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SubTask(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название подзадачи",
    )
    description = models.TextField(blank=True, verbose_name="Описание подзадачи")
    status = models.CharField(
        max_length=20,
        choices=Task.STATUS_CHOICES,
        default="New",
        verbose_name="Статус",
    )
    deadline = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дедлайн",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="subtasks",
        verbose_name="Основная задача",
    )

    class Meta:
        db_table = "task_manager_subtask"
        verbose_name = "SubTask"
        verbose_name_plural = "SubTasks"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
