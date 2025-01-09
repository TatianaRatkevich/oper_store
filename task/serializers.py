from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()
    processed_by = serializers.StringRelatedField(allow_null=True)
    images_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    def get_images_count(self, obj):
        return obj.images.count()
