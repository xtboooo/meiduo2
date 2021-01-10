from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework import mixins
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from meiduo_admin.serializers.users import AdminAuthSerializer, UserSerializer

# POST /meiduo_admin/authorizations/
from users.models import User


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


# GET /meiduo_admin/?page=<页码>&pagesize=<页容量>&keyword=<搜索内容>
class UserInfoView(ListAPIView):
    # 指定权限：只有管理员用户才能进行访问
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        """返回视图所使用的查询集"""
        # 1.获取 keyword 关键字
        # self.request：获取请求对象
        keyword = self.request.query_params.get('keyword')

        # 2.查询普通用户数据
        if keyword:
            users = User.objects.filter(is_staff=False, username__contains=keyword)
        else:
            users = User.objects.filter(is_staff=False)
        return users

    # def get(self, request):
    #     """普通用户数据查询"""
        # # 1.查询普通用户数据
        # users = self.get_queryset()
        #
        # # ② 将用户数据序列化并返回
        # serializer = self.get_serializer(users, many=True)
        # return Response(serializer.data)
        # return self.list(request)
