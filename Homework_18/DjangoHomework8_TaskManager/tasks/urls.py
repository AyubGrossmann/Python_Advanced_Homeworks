from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    TaskListCreateAPIView,
    TaskRetrieveUpdateDestroyAPIView,
    TaskStatisticsAPIView,
    SubTaskListCreateView,
    SubTaskRetrieveUpdateDestroyView,
    CategoryViewSet,
)

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Маршруты для задач.
    path("tasks/", TaskListCreateAPIView.as_view(), name="task-list-create"),
    path("tasks/statistics/", TaskStatisticsAPIView.as_view(), name="task-statistics"),
    path(
        "tasks/<int:pk>/",
        TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task-detail",
    ),

    # Маршруты для подзадач.
    path("subtasks/", SubTaskListCreateView.as_view(), name="subtask-list-create"),
    path(
        "subtasks/<int:pk>/",
        SubTaskRetrieveUpdateDestroyView.as_view(),
        name="subtask-detail",
    ),

    # CRUD-маршруты категорий из DefaultRouter.
    path("", include(router.urls)),
]
