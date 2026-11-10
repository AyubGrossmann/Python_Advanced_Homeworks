from django.utils import timezone
from rest_framework import serializers

from .models import Task, SubTask, Category


class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class SubTaskCreateSerializer(serializers.ModelSerializer):
    # Дата создания заполняется автоматически и доступна только для чтения.
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = [
            "id",
            "title",
            "description",
            "task",
            "status",
            "deadline",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

    def validate_name(self, value):
        # При создании проверяем, что категория с таким названием не существует.
        if Category.all_objects.filter(name=value).exists():
            raise serializers.ValidationError(
                "Категория с таким названием уже существует."
            )
        return value

    def create(self, validated_data):
        # Создаём категорию после проверки уникальности.
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # При обновлении не считаем текущую категорию дубликатом самой себя.
        new_name = validated_data.get("name", instance.name)

        if Category.all_objects.filter(name=new_name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                {"name": "Категория с таким названием уже существует."}
            )

        instance.name = new_name
        instance.save()
        return instance


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_deadline(self, value):
        # Дедлайн не может находиться в прошлом.
        if value is not None and value < timezone.now():
            raise serializers.ValidationError(
                "Дедлайн не может быть в прошлом."
            )
        return value


class TaskDetailSerializer(serializers.ModelSerializer):
    # Показываем все подзадачи, связанные с этой задачей.
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "created_at",
            "categories",
            "subtasks",
        ]
        read_only_fields = ["id", "created_at"]
