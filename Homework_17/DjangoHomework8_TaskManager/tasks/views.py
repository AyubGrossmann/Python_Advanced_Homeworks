from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Task, SubTask, Category
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    SubTaskSerializer,
    SubTaskCreateSerializer,
    CategoryCreateSerializer,
)


class TaskListCreateAPIView(generics.ListCreateAPIView):
    # GET — список задач, POST — создание новой задачи.
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Фильтрация по статусу и дедлайну.
    filterset_fields = ["status", "deadline"]

    # Поиск по названию и описанию.
    search_fields = ["title", "description"]

    # Сортировка по дате создания.
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TaskCreateSerializer
        return TaskDetailSerializer


class TaskRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    # GET — получение, PUT/PATCH — обновление, DELETE — удаление задачи.
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


class TaskStatisticsAPIView(APIView):
    # GET — статистика задач. Этот endpoint оставляем из ДЗ №12.
    def get(self, request):
        total_tasks = Task.objects.count()

        tasks_by_status = Task.objects.values("status").annotate(
            total=Count("id")
        )

        status_statistics = {}
        for item in tasks_by_status:
            status_statistics[item["status"]] = item["total"]

        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now()
        ).exclude(status="Done").count()

        return Response({
            "total_tasks": total_tasks,
            "tasks_by_status": status_statistics,
            "overdue_tasks": overdue_tasks,
        })


class SubTaskListCreateView(generics.ListCreateAPIView):
    # GET — список подзадач, POST — создание подзадачи.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Фильтрация по статусу и дедлайну.
    filterset_fields = ["status", "deadline"]

    # Поиск по названию и описанию.
    search_fields = ["title", "description"]

    # Сортировка по дате создания.
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # GET — получение, PUT/PATCH — обновление, DELETE — удаление подзадачи.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer



class CategoryViewSet(viewsets.ModelViewSet):
    # ModelViewSet автоматически предоставляет CRUD для категорий.
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=True, methods=["get"])
    def count_tasks(self, request, pk=None):
        # Получаем категорию и считаем связанные с ней задачи.
        category = self.get_object()
        tasks_count = category.tasks.count()

        return Response({
            "category_id": category.id,
            "category_name": category.name,
            "tasks_count": tasks_count,
        })
