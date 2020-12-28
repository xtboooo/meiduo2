import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection
from haystack.query import SearchQuerySet

from goods.models import GoodsCategory, SKU
from goods.utils import get_breadcrumb

# GET /list/(?P<category_id>\d+)/skus/
from meiduo_mall.utils.mixins import LoginRequiredMixin


class SKUListView(View):
    def get(self, request, category_id):
        """ 分类商品数据获取 """
        # 1.获取参数并进行校验
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        ordering = request.GET.get('ordering', '-create_time')

        # 查询数据库获得指定id的商品分类对象
        try:
            cat3 = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 400,
                                 'message': '分类数据不存在!'})

        # 2.查询获取商品列表页相关数据
        # 面包屑导航数据
        try:
            breadcrumb = get_breadcrumb(cat3)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '面包屑导航数据获取错误!'})

        # 分类SKU商品数据
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True, ).order_by(ordering)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '分类SKU商品数据获取错误'})

        # 3.对SKU商品数据进行分页
        paginator = Paginator(skus, page_size)
        results = paginator.get_page(page)

        sku_li = []

        # FastDFS 中 nginx 服务器的地址
        nginx_url = 'http://192.168.19.131:8888/'

        for sku in results:
            sku_li.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'comments': sku.comments,
                'default_image_url': nginx_url + sku.default_image.name,
            })

        # 4.返回响应数据
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'breadcrumb': breadcrumb,
                             'count': paginator.num_pages,
                             'list': sku_li, })


# GET /search/?q=<关键字>&page=<页码>&page_size=<页容量>
class SKUSearchView(View):
    def get(self, requset):
        """ SKU商品数据搜索 """
        # 1.获取参数并进行校验
        keyword = requset.GET.get('q')
        page = requset.GET.get('page', 1)
        page_size = requset.GET.get('page_size', 6)

        if not keyword:
            return JsonResponse({'code': 400,
                                 'message': '缺少搜索关键字!'})

        # 2.使用haystack检索数据
        query = SearchQuerySet()
        search_res = query.auto_query(keyword).load_all()

        # 3.对结果数据进行分页
        paginator = Paginator(search_res, page_size)
        results = paginator.get_page(page)

        # 4.组织响应数据并返回
        sku_li = []
        nginx_url = 'http://192.168.19.131:8888/'

        for res in results:
            sku = res.object
            sku_li.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': nginx_url + sku.default_image.name,
                'comments': sku.comments,
            })

        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'count': paginator.count,
                             'page_size': paginator.per_page,
                             'query': keyword,
                             'skus': sku_li, })


# GET /hot/(?P<category_id>\d+)/
class GetHotSKUView(View):
    def get(self, request, category_id):
        """ 获取当前分类下的 TOP2 热销商品数据 """
        # 1.获取三级分类下所有的SKU,按销量降序排序取并前两位
        try:
            skus = SKU.objects.filter(category_id=category_id,
                                      is_launched=True).order_by('-sales')[:2]
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '分类SKU商品数据获取错误'})
        hot_skus = []

        # FastDFS 中 nginx 服务器的地址
        nginx_url = 'http://192.168.19.131:8888/'

        for sku in skus:
            hot_sku = {
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image_url': nginx_url + sku.default_image.name,
            }
            hot_skus.append(hot_sku)

        # 3.返回响应
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'hot_skus': hot_skus})


# POST/GET /browse_histories/
class SKUBrowseHistoriesView(LoginRequiredMixin, View):
    def post(self, request):
        """
        保存sku商品的浏览记录
        1. 获取参数并进行校验
        2. 尝试删除该用户redis列表中的该商品
        3. 最左侧新增商品id
        4. 只保留前五条记录
        5. 返回响应
        # redis list 数据操作相关指令
        # lrem key count value：从 list 列列表中移除指定的 value 元素，count 表示移除⼏几次
        # 1）count = 0 : 移除 list 所有与 value 相等的元素。
        # 2）count > 0 : 从 list 由左向右移除 value 元素，最多移除 count 次
        # 3）count < 0 : 从 list 由右向左移除 value 元素，最多移除 count 次
        # lpush key member ...：从 list 列列表左侧添加元素
        # ltrim key start stop：保存 list 列列表指定范围内[start, stop]的元素，
        """
        # 1. 获取参数并进行校验
        user = request.user
        req_data = json.loads(request.body)
        sku_id = req_data.get('sku_id')

        if not sku_id:
            return JsonResponse({'code': 400,
                                 'message': '缺少必传参数sku_id'})
        try:
            sku = SKU.objects.get(id=sku_id, is_launched=True)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '获取sku商品出错'})

        redis_conn = get_redis_connection('browse_histories')
        pl = redis_conn.pipeline()
        try:
            # 2. 尝试删除该用户redis列表中的该商品
            pl.lrem('history_%s' % user.id, count=0, value=sku_id)

            # 3.最左侧新增商品id
            # history_ <⽤用户id >: ["浏览的商品id", "浏览的商品id", ...]
            pl.lpush('history_%s' % user.id, sku_id)

            # 4. 只保留前五条记录
            pl.ltrim('history_%s' % user.id, 0, 5)
            pl.execute()
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '保存sku浏览记录出错'})
        return JsonResponse({'code': 0,
                             'message': 'OK'})

    def get(self, request):
        """
        用户浏览记录获取
        1. 获取当前登录用户浏览记录中5条最新sku商品的id
        2. 组织响应
        3. 返回响应
        # redis list 数据操作相关指令
        lrange key start stop：获取 list 列列表指定范围内[start, stop]的元素
        """
        # 1. 获取当前登录用户浏览记录中5条最新sku商品的id
        user = request.user
        redis_conn = get_redis_connection('browse_histories')
        try:
            sku_ids = redis_conn.lrange('history_%s' % user.id, 0, 5)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '获取商品浏览记录出错!'})
        sku_li = []
        try:
            for sku_id in sku_ids:
                sku = SKU.objects.get(id=sku_id, is_launched=True)
                sku_li.append({
                    'id': sku.id,
                    'name': sku.name,
                    'price': sku.price,
                    'comments': sku.comments,
                    'default_image_url': 'http://192.168.19.131:8888/' + sku.default_image.name
                })
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '查询sku商品出错!'})
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'skus': sku_li})
