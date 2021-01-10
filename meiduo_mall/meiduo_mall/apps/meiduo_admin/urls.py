from django.urls import re_path
from meiduo_admin.views import users, statistical

urlpatterns = [
    # 管理员登陆
    re_path(r'^authorizations/$', users.AdminAuthorizeView.as_view()),

    # 数据统计
    re_path(r'^statistical/day_active/$', statistical.UserDayActiveView.as_view()),

]