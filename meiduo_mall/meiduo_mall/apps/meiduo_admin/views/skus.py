from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU, SPU, SPUSpecification
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer, SPUSimpleSerializer, \
    SPUSpecSerializer


class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer


class SKUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer
    pagination_class = None


class SKUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SKUSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword == '' or keyword is None:
            return SKU.objects.all()
        else:
            return SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))


# GET /meiduo_admin/goods/simple/
class SPUSimpleView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSimpleSerializer
    pagination_class = None


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = SPUSpecSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = SPUSpecification.objects.filter(spu_id=self.kwargs.get('pk'))
        return queryset
