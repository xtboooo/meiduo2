from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.permissions import PermissionSerializer, ContentTypeSerializer


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    def content_types(self, request):
        """获取权限类型数据"""
        # ① 获取权限类型数据
        content_types = ContentType.objects.all()

        # ② 将权限类型数据序列化并返回
        serializer = ContentTypeSerializer(content_types, many=True)

        return Response(serializer.data)
