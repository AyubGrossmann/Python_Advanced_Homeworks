from django.db.models import Count
from django.utils import timezone
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # GET — список задач, POST — создание новой задачи.
    queryset = Task.objects.all()

    def get_queryset(self):
        # Пользователь получает только свои задачи.
        if self.request.user.is_authenticated:
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # GET — получение, PUT/PATCH — обновление, DELETE — удаление задачи.
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()


class TaskStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # GET — статистика задач. Этот endpoint оставляем из ДЗ №12.
    def get(self, request):
        user_tasks = Task.objects.filter(owner=request.user)
        total_tasks = user_tasks.count()

        tasks_by_status = user_tasks.values("status").annotate(
            total=Count("id")
        )

        status_statistics = {}
        for item in tasks_by_status:
            status_statistics[item["status"]] = item["total"]

        overdue_tasks = user_tasks.filter(
            deadline__lt=timezone.now()
        ).exclude(status="Done").count()

        return Response({
            "total_tasks": total_tasks,
            "tasks_by_status": status_statistics,
            "overdue_tasks": overdue_tasks,
        })


class SubTaskListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # GET — список подзадач, POST — создание подзадачи.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SubTask.objects.filter(owner=self.request.user)
        return SubTask.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Фильтрация по статусу и дедлайну.
    filterset_fields = ["status", "deadline"]

    # Поиск по названию и описанию.
    search_fields = ["title", "description"]

    # Сортировка по дате создания.
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class SubTaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    # GET — получение, PUT/PATCH — обновление, DELETE — удаление подзадачи.
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return SubTask.objects.filter(owner=self.request.user)
        return SubTask.objects.none()



class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
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
