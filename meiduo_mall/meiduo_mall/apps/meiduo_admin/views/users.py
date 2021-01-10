from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from meiduo_admin.serializers.users import AdminAuthSerializer


# POST /meiduo_admin/authorizations/
class AdminAuthorizeView(CreateAPIView):
    serializer_class = AdminAuthSerializer
    # def post(self, request):
    #     """管理员登录"""
    #     # ① 获取参数并进行校验
    #     serializer = AdminAuthSerializer(data=request.data)
    #     serializer.is_valid()
    #
    #     # ② 服务器生成 jwt token 数据
    #     # 调用序列化器类中的 create，将生成 JWT token 的代码抽取到了序列化器类的 create 方法中
    #     serializer.save()
    #
    #     # ③ 返回响应
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
