from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

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

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    username_filter = request.GET.get('username')

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

    return render(request, 'task/rejected_tasks.html', {
        'tasks': tasks,
        'start_date': start_date,
        'end_date': end_date,
        'username_filter': username_filter,
        'store_users': store_users,  # Передаём список пользователей store
    })

