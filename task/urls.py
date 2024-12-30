from django.urls import path, include
from .views import create_task, rejected_tasks_view, process_task_view
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')


urlpatterns = [
    path('', include(router.urls)),
    path('create/', create_task, name='create_task'),
    path('rejected_tasks/', rejected_tasks_view, name='rejected_tasks'),
    path('tasks/<int:task_id>/process/', process_task_view, name='process_task'),
]
