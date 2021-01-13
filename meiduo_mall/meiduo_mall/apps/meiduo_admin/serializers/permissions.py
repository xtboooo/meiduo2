from django.contrib.auth.models import Permission
from rest_framework import serializers


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器类"""

    class Meta:
        model = Permission
        fields = '__all__'
