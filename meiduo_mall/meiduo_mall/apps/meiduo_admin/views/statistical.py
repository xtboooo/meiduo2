from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
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


# GET /meiduo_admin/statistical/month_increment/
class UserMonthCountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        """ 30天每日新增用户统计 """
        # 1.查询数据库统计网站近 30 天每日新增用户数量

        # 结束时间
        now_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # 起始时间: now_date - 29天
        start_time = now_time - timezone.timedelta(days=29)

        # 当天日期
        current_date = start_time

        # 每日新增用户的数量
        month_li = []

        while current_date <= now_time:
            # 次日时间
            next_date = current_date + timezone.timedelta(days=1)

            # 统计当天的新增用户数量
            count = User.objects.filter(date_joined__gte=current_date,
                                        date_joined__lte=next_date).count()

            month_li.append({
                'count': count,
                'date': current_date.date()
            })

            current_date = next_date

        # 2.返回响应数据
        return Response(month_li)


# GET /meiduo_admin/statistical/total_count/
class UserTotalCountView(APIView):
    def get(self, request):
        now_time = timezone.now()
        count = User.objects.filter(is_staff=False).count()
        return Response({
            'date': now_time.date(),
            'count': count
        })


# GET /meiduo_admin/statistical/day_increment/
class UserDayIncreCountView(APIView):
    def get(self, request):
        now_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(date_joined__gte=now_time).count()
        return Response({
            'date': now_time.date(),
            'count': count
        })


# GET /meiduo_admin/statistical/goods_day_views/
class GoodsDayViewsCountView(APIView):
    def get(self, request):
        goods = GoodsVisitCount.objects.all()

        goods_li = []

        for good in goods:
            goods_li.append({
                'category': good.category.name,
                'count': good.count
            })

        return Response(goods_li)
