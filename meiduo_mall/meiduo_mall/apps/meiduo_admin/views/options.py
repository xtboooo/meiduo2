from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializers.options import OptionSerializer, SpecSimpleSerializer


class OptionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    look_value_regex = '\d+'
    queryset = SpecificationOption.objects.all()
    serializer_class = OptionSerializer


# GET /meiduo_admin/goods/specs/simple/
class SpecSimpleView(ListAPIView):
    """获取简单规格数据"""
    permission_classes = [IsAdminUser]
    queryset = SPUSpecification.objects.all()
    serializer_class = SpecSimpleSerializer
    pagination_class = None
