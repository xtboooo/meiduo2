from rest_framework import serializers

from users.models import User


class AdminAuthSerializer(serializers.ModelSerializer):
    """管理员序列化器类"""

    # 注意：模型类中有，但是自己想重新进行定义的字段，也可以这样直接进行添加
    username = serializers.CharField(label='用户名')

    # 注意：模型类中没有，而序列化器类中又需要的字段，可以自己直接进行添加，但自己添加的字段也要放到 fields 中
    token = serializers.CharField(label='JWT token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        # 补充校验
        username = attrs['username']
        password = attrs['password']

        # 进行用户名和密码校验
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

            attrs['user'] = user

        return attrs

    def create(self, validated_data):
        # 获取登录用户 user
        user = validated_data['user']

        # 服务器生成 jwt token, 保存当前用户的身份信息
        from rest_framework_jwt.settings import api_settings

        # 组织 payload 数据的方法
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER

        # 生成 jwt token 数据的方法
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        # 组织 payload 数据
        payload = jwt_payload_handler(user)
        # 生成 jwt token
        token = jwt_encode_handler(payload)

        # 给 user 对象增加临时属性，保存 jwt token 的数据
        user.token = token

        return user


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email')
