from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage
from meiduo_admin.serializers.skus import SKUImageSerializer


class SKUImageViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer
