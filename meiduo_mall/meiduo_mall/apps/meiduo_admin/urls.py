from rest_framework.routers import SimpleRouter

from django.urls import re_path
from meiduo_admin.views import users, statistical, skus, permissions, channels, spus

urlpatterns = [
    # 用户管理-管理员登陆
    re_path(r'^authorizations/$', users.AdminAuthorizeView.as_view()),

    # 用户管理-新增普通用户
    re_path(r'^users/$', users.UserInfoView.as_view()),

    # 数据统计
    re_path(r'^statistical/day_active/$', statistical.UserDayActiveView.as_view()),
    re_path(r'^statistical/day_orders/$', statistical.UserDayOrdersView.as_view()),
    re_path(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    re_path(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    re_path(r'^statistical/day_increment/$', statistical.UserDayIncreCountView.as_view()),
    re_path(r'^statistical/goods_day_views/$', statistical.GoodsDayViewsCountView.as_view()),

    # 用户管理
    re_path(r'^users/$', users.UserInfoView.as_view()),

    # 图片管理
    re_path(r'^skus/simple/$', skus.SKUSimpleView.as_view()),

    # 商品管理-频道管理-获取频道组数据
    re_path(r'^goods/channel_types/$', channels.ChannelTypeView.as_view()),

    # 商品管理-频道管理-获取一二三级商品分类
    re_path('^goods/categories/$', channels.Category123View.as_view()),
    re_path('^goods/channel/categories/$', channels.Category123View.as_view()),
    re_path('^goods/channel/categories/(?P<pk>\d+)/$', channels.Category123View.as_view()),

    # 商品管理-spu商品管理-获取品牌数据
    re_path('^goods/brands/simple/$', spus.BrandView.as_view()),

    # 商品管理-spu商品管理-上传spu图片
    # TODO: 上传spu图片

    # 权限管理-权限类型数据获取
    re_path(r'^permission/content_types/$', permissions.PermissionViewSet.as_view({
        'get': 'content_types'
    })),

    # 用户组管理-权限简单数据获取
    re_path(r'^permission/simple/$', permissions.GroupViewSet.as_view({
        'get': 'simple'
    })),

    # 管理员管理-用户组简单数据获取
    re_path(r'^permission/groups/simple/$', permissions.AdminViewSet.as_view({
        'get': 'simple'
    }))

]

router = SimpleRouter()

# 商品管理-sku商品图片管理
router.register('skus/images', skus.SKUImageViewSet, basename='images')

# 商品管理-频道管理
router.register('goods/channels', channels.ChannelViewSet, basename='channels')

# 商品管理-spu商品管理
router.register('goods', spus.SPUViewSet, basename='spus')

# 商品管理-sku商品管理
router.register('skus', skus.SKUViewSet, basename='skus')

# 系统管理-权限数据管理
router.register('permission/perms', permissions.PermissionViewSet, basename='perms')

# 系统管理-用户组数据管理
router.register('permission/groups', permissions.GroupViewSet, basename='groups')

# 系统管理-管理员数据管理
router.register('permission/admins', permissions.AdminViewSet, basename='admins')

urlpatterns += router.urls
# for url in router.urls:
#     print(url)
