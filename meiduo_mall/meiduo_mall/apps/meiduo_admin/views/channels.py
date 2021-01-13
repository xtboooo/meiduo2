from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel
from meiduo_admin.serializers.channels import ChannelSerializer


class ChannelViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = GoodsChannel.objects.all()
    serializer_class = ChannelSerializer
