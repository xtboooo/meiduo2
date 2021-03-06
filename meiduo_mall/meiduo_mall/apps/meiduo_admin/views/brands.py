from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brands import BrandSerializer


class BrandViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
