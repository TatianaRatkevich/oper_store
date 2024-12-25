from django.contrib import admin
from .models import Task, Image

class ImageInline(admin.TabularInline):
    """
    Вспомогательный класс для отображения связанных изображений в задаче.
    """
    model = Image
    extra = 1  # Количество пустых полей для добавления новых изображений
    readonly_fields = ('image',)  # Делаем поле только для чтения

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Task в админке.
    """
    list_display = ('id', 'status', 'created_by', 'processed_by', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at', 'created_by', 'processed_by')
    search_fields = ('id', 'comment', 'created_by__username', 'processed_by__username')
    ordering = ('-created_at',)  # Сортировка по дате создания (новые сверху)
    inlines = [ImageInline]  # Включаем связанные изображения
    readonly_fields = ('created_at', 'updated_at')  # Поля только для чтения

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """
    Класс для настройки отображения модели Image в админке.
    """
    list_display = ('id', 'task', 'image')
    list_filter = ('task',)
    search_fields = ('task__id', 'task__comment')
