from rest_framework.routers import SimpleRouter

from django.urls import re_path
from meiduo_admin.views import users, statistical, skus

urlpatterns = [
    # 管理员登陆
    re_path(r'^authorizations/$', users.AdminAuthorizeView.as_view()),

    # 数据统计
    re_path(r'^statistical/day_active/$', statistical.UserDayActiveView.as_view()),
    re_path(r'^statistical/day_orders/$', statistical.UserDayOrdersView.as_view()),
    re_path(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),

    # 用户管理
    re_path(r'^users/$', users.UserInfoView.as_view()),

]

router = SimpleRouter()
router.register('skus/images', skus.SKUImageViewSet, basename='images')
urlpatterns += router.urls
for url in router.urls:
    print(url)
