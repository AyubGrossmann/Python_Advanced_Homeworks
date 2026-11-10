from django.db import models
from django.utils import timezone


class ActiveCategoryManager(models.Manager):
    # По умолчанию показываем только категории, которые не удалены.
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалена")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата удаления")

    # objects — только активные категории.
    objects = ActiveCategoryManager()

    # all_objects — все категории, включая удалённые.
    all_objects = models.Manager()

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def delete(self, using=None, keep_parents=False):
        # Вместо физического удаления помечаем категорию как удалённую.
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at"])
        return (1, {self._meta.label: 1})
