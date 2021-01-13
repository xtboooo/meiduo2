from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from users.models import User


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器类"""

    class Meta:
        model = Permission
        fields = '__all__'


class ContentTypeSerializer(serializers.ModelSerializer):
    """权限类型序列化器类"""

    class Meta:
        model = ContentType
        fields = ('id', 'name')


class GroupSerializer(serializers.ModelSerializer):
    """用户组序列化器类"""

    class Meta:
        model = Group
        fields = '__all__'


class PermissionSimpleSerializer(serializers.ModelSerializer):
    """简单权限数据序列化器类"""

    class Meta:
        model = Permission
        fields = ('id', 'name')


class AdminSerializer(serializers.ModelSerializer):
    """管理员序列化器类"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile', 'groups', 'user_permissions', 'password')

        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False,
                # 数据校验时，允许 password 传递空字符串
                'allow_blank': True,
            }
        }

    def create(self, validated_data):
        """创建管理员用户"""
        # 设置管理员标记 is_staff 为 True
        validated_data['is_staff'] = True

        # 1.调用 ModelSerializer 中的 create 方法进行管理员用户数据的保存
        user = super().create(validated_data)

        # 2.判断是否需要设置默认密码，并对密码进行加密保存
        password = validated_data.get('password')
        if not password:
            # 管理员默认密码
            password = '123456abc'

        user.set_password(password)
        user.save()

        return user


class GroupSimpleSerializer(serializers.ModelSerializer):
    """用户组简单数据序列化器类"""

    class Meta:
        model = Group
        fields = ('id', 'name')
