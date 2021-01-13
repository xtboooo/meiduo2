from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU
from meiduo_admin.serializers.spus import SPUSerializer


class SPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SPU.objects.all()
    serializer_class = SPUSerializer
