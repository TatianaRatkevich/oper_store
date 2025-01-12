from tkinter.font import names

from django.urls import path, include
from .views import create_task, rejected_tasks_view, process_task_view
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, RejectedTaskViewSet, show_task, image_detail


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'rejected_tasks', RejectedTaskViewSet, basename='rejected_task')


urlpatterns = [
    path('rejected_tasks/', rejected_tasks_view, name='rejected_tasks'),
    path('', include(router.urls)),
    path('create/', create_task, name='create_task'),
    path('task/<int:task_id>/', show_task, name='show_task'),
    path('tasks/<int:task_id>/process/', process_task_view, name='process_task'),
    path('task/<int:task_id>/image/<int:image_id>', image_detail, name='image_detail')
]
