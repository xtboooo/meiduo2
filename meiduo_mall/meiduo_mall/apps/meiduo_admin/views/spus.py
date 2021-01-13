from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import SPU, Brand
from meiduo_admin.serializers.spus import SPUSerializer, BrandSerializer


class SPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SPU.objects.all()
    serializer_class = SPUSerializer


# GET /meiduo_admin/goods/brands/simple/
class BrandView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None
