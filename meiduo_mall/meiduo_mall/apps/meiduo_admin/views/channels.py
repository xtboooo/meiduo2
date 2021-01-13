from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from goods.models import GoodsChannel, GoodsChannelGroup
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelTypeSerializer


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
