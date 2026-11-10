from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


class SubTaskInline(admin.TabularInline):
    # Позволяет создавать подзадачи прямо при создании или редактировании задачи.
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # В списке показываем короткое название, чтобы длинные названия не мешали.
    list_display = ("id", "short_title", "status", "deadline", "created_at")
    list_filter = ("status", "categories")
    search_fields = ("title", "description")
    filter_horizontal = ("categories",)
    readonly_fields = ("created_at",)
    inlines = [SubTaskInline]

    @admin.display(description="Название задачи", ordering="title")
    def short_title(self, obj):
        # Если название длиннее 10 символов, показываем первые 10 и многоточие.
        if len(obj.title) > 10:
            return obj.title[:10] + "..."
        return obj.title


@admin.action(description="Отметить выбранные подзадачи как Done")
def mark_subtasks_as_done(modeladmin, request, queryset):
    # Одним запросом меняем статус всех выбранных подзадач.
    updated_count = queryset.update(status="Done")
    modeladmin.message_user(
        request,
        f"Статус Done установлен для {updated_count} подзадач."
    )


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    search_fields = ("title", "description", "task__title")
    readonly_fields = ("created_at",)
    actions = [mark_subtasks_as_done]
