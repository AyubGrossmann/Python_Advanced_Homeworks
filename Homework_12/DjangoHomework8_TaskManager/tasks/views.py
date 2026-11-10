from django.db.models import Count
from django.utils import timezone
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


class TaskListCreateAPIView(generics.ListCreateAPIView):
    # GET /api/tasks/ — список задач.
    # POST /api/tasks/ — создание задачи.
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskDetailAPIView(generics.RetrieveAPIView):
    # GET /api/tasks/<id>/ — одна задача по ID.
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskStatisticsAPIView(APIView):
    # GET /api/tasks/statistics/ — статистика задач.
    def get(self, request):
        total_tasks = Task.objects.count()

        # Считаем количество задач отдельно для каждого статуса.
        tasks_by_status = Task.objects.values("status").annotate(
            total=Count("id")
        )

        status_statistics = {}
        for item in tasks_by_status:
            status_statistics[item["status"]] = item["total"]

        # Просроченные задачи: дедлайн прошёл, задача ещё не завершена.
        overdue_tasks = Task.objects.filter(
            deadline__lt=timezone.now()
        ).exclude(status="Done").count()

        data = {
            "total_tasks": total_tasks,
            "tasks_by_status": status_statistics,
            "overdue_tasks": overdue_tasks,
        }

        return Response(data)
