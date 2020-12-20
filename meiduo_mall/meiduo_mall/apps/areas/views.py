from django.http import JsonResponse
from django.views import View
from areas.models import Areas


# GET /areas/
class ProvinceAreasView(View):
    def get(self, request):
        """ 获取所有地区的省级地区信息"""
        # 1.查询数据库所有省级地区信息
        try:
            provinces = Areas.objects.filter(parent=None).values('id', 'name')
            # 将QuerySet中的数据转换为列表
            provinces = list(provinces)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '省级信息获取错误!'})

        # 2.组织数据信息并返回响应
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'provinces': provinces, })


# GET /areas/(?P<pk>\d+)/
class SubAreasView(View):
    def get(self, request, pk):
        """ 获取指定地区的下级地区信息 """
        # 1.根据pk获取指定地区的下级地区信息
        try:
            subs_li = Areas.objects.filter(parent_id=pk).values('id', 'name')
            # 将QuerySet中的数据转换为列表
            subs_li = list(subs_li)
        except Exception as e:
            return JsonResponse({'code': 400,
                                 'message': '子级地区信息获取错误!'})

        # 2.组织数据并进行返回
        return JsonResponse({'code': 0,
                             'message': 'OK',
                             'subs': subs_li})
