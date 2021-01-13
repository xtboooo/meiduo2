from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from meiduo_admin.serializers.permissions import PermissionSerializer, ContentTypeSerializer, GroupSerializer, \
    PermissionSimpleSerializer, AdminSerializer, GroupSimpleSerializer
from users.models import User


class PermissionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # lookup_value_regex = '\d+'
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

    # GET /meiduo_admin/permission/content_types/ -> content_types
    def content_types(self, request):
        """获取权限类型数据"""
        # 1.获取权限类型数据
        content_types = ContentType.objects.all()

        # 2.将权限类型数据序列化并返回
        serializer = ContentTypeSerializer(content_types, many=True)

        return Response(serializer.data)


class GroupViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # lookup_value_regex = '\d+'
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    # GET /meiduo_admin/permission/simple/ -> simple
    def simple(self, request):
        """获取权限数据"""
        # 1.获取权限数据
        permissions = Permission.objects.all()

        # 2.将权限数据序列化并返回
        serializer = PermissionSimpleSerializer(permissions, many=True)
        return Response(serializer.data)


class AdminViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    # lookup_value_regex = '\d+'
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminSerializer

    # GET /meiduo_admin/permission/groups/simple/ -> simple
    def simple(self, request):
        """获取用户组数据"""
        # 1.获取用户组数据
        groups = Group.objects.all()

        # 2.将用户组数据序列化并返回
        serializer = GroupSimpleSerializer(groups, many=True)
        return Response(serializer.data)
