from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from goods.models import SPU, Brand
from meiduo_admin.serializers.spus import SPUSerializer, BrandSerializer, SPUImageSerializer


class SPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SPU.objects.all()
    serializer_class = SPUSerializer

    @action(methods=['post'], detail=False)
    def images(self, request):
        serializer = SPUImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        res = client.upload_by_buffer(request.data.get('image').read())
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FDFS失败')
        file_id = res.get('Remote file_id')

        return Response({
            'img_url': settings.FDFS_URL + file_id
        })


# GET /meiduo_admin/goods/brands/simple/
class BrandView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None
