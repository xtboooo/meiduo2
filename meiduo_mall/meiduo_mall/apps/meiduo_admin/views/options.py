from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption
from meiduo_admin.serializers.options import OptionSerializer


class OptionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    look_value_regex = '\d+'
    queryset = SpecificationOption.objects.all()
    serializer_class = OptionSerializer
