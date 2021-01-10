from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


# GET /meiduo_admin/statistical/day_active/
class UserDayActiveView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ 获取网站日活跃用户数 """
        # 1.查询数据库统计网站当日活跃用户数
        now_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gte=now_time).count()

        # 2.返回响应数据
        return Response({
            'date': now_time.date(),
            'count': count
        })


# GET /meiduo_admin/statistical/day_orders/
class UserDayOrdersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ 获取网站日下单用户数 """
        # 1.查询数据库统计网站当日下单用户数
        now_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(orders__create_time__gte=now_time).distinct().count()

        # 2.返回响应数据
        return Response({
            'date': now_time.date(),
            'count': count
        })
