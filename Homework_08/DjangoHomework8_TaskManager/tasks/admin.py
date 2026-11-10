from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "deadline", "created_at")
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at",)
    inlines = [SubTaskInline]


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "task__title")
    readonly_fields = ("created_at",)
