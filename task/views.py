from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .serializers import TaskSerializer
from .forms import TaskForm
from .models import Image, Task


@login_required
def create_task(request):
    if request.user.role != 'store':
        messages.error(request, 'Только магазины могут создавать задачи.')
        return redirect('role_redirect')  # Перенаправление в случае отсутствия прав

    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task = task_form.save(commit=False)
            task.created_by = request.user
            task.save()

            images = request.FILES.getlist('images')  # Получаем все загруженные изображения
            for img in images:
                Image.objects.create(task=task, image=img)

            messages.success(request, 'Задача успешно создана.')
            return redirect('store_index')  # Перенаправление после успешного создания задачи
    else:
        task_form = TaskForm()

    context = {'task_form': task_form}
    return render(request, 'task/create_task.html', context)


@login_required
def rejected_tasks_view(request):
    """
    View для отображения отклоненных задач.
    """
    User = get_user_model()
    tasks = Task.objects.filter(status='rejected').order_by('-created_at')

    start_date = request.GET.get('start_date') or None
    end_date = request.GET.get('end_date') or None
    username_filter = request.GET.get('username') or ''
    page_number = request.GET.get('page', 1)

    # Фильтрация по дате
    if start_date and end_date:
        tasks = tasks.filter(
            created_at__date__gte=start_date,
            created_at__date__lte=end_date
        )

    # Дополнительная фильтрация для операторов
    if request.user.role == 'operator':
        store_users = User.objects.filter(role='store')  # Получаем всех пользователей с ролью store
        if username_filter:
            tasks = tasks.filter(created_by__username=username_filter)
    else:
        tasks = tasks.filter(created_by=request.user)  # Пользователи store видят только свои задачи
        store_users = None  # У store нет фильтра по пользователям

    # Пагинация
    paginator = Paginator(tasks, 20)
    page_obj = paginator.get_page(page_number)

    return render(request, 'task/rejected_tasks.html', {
        'tasks': page_obj,
        'start_date': start_date,
        'end_date': end_date,
        'username_filter': username_filter,
        'store_users': store_users,  # Передаём список пользователей store
    })


@login_required
def process_task_view(request, task_id):
    """
    View для обработки задачи оператором.
    """
    task = get_object_or_404(Task, id=task_id)

    # Ограничение доступа для не операторов
    if request.user.role != 'operator':
        return redirect('role_redirect')

    # Проверка: задача уже обрабатывается другим оператором
    if task.processed_by and task.processed_by != request.user:
        messages.error(request, f"Задача уже обрабатывается оператором: {task.processed_by.username}")
        return redirect('operator_index')

    # Разрешить оператору взять задачу в обработку, если она имеет статус "pending"
    if task.status == 'pending':
        try:
            task.assign_to_operator(request.user)
        except ValidationError as e:
            return HttpResponseForbidden(f"Ошибка: {e}")

    # Если задача не имеет статус "in_progress" после назначения, перенаправляем обратно
    if task.status != 'in_progress':
        return redirect('operator_index')

    error_message = None

    # Управление статусами задачи
    if request.method == 'POST':
        action = request.POST.get('action')

        try:
            if action == 'complete':
                task.mark_as_completed()
            elif action == 'reject':
                task.mark_as_rejected()
            elif action == 'return':
                task.status = 'pending'
                task.processed_by = None
                task.save()
            return redirect('operator_index')
        except ValidationError as e:
            error_message = str(e)

    return render(request, 'task/task_process.html', {
        'task': task,
        'error_message': error_message
    })


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('created_at')
    serializer_class = TaskSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20


class RejectedTaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.filter(status='rejected').order_by('-created_at')
    serializer_class = TaskSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


def show_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task/show_task.html', {'task': task})


def image_detail(request, task_id, image_id):
    task = get_object_or_404(Task, id=task_id)
    image = get_object_or_404(Image, id=image_id, task=task)
    return render(request, 'task/image_detail.html', {'task': task, 'image': image})