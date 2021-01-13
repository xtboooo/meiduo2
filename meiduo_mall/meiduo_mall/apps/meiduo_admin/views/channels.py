from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelTypeSerializer, Category123Serializer


class ChannelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = GoodsChannel.objects.all()
    serializer_class = ChannelSerializer


# GET /meiduo_admin/goods/channel_types/
class ChannelTypeView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = ChannelTypeSerializer
    pagination_class = None


# GET /meiduo_admin/goods/categories/
class Category123View(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = Category123Serializer
    pagination_class = None

    def get_queryset(self):
        queryset = GoodsCategory.objects.filter(parent_id=self.kwargs.get('pk', None))
        return queryset
