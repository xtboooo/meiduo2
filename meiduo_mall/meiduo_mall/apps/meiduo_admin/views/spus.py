from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.decorators import action
from goods.models import SPU, Brand
from meiduo_admin.serializers.spus import SPUSerializer, BrandSerializer, SPUImageSerializer
from meiduo_mall.utils.fastdfs.storage import FastDFSStorage


class SPUViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    queryset = SPU.objects.all()
    serializer_class = SPUSerializer

    # POST /meiduo_admin/goods/images/ -> images
    @action(methods=['post'], detail=False)
    def images(self, request):
        serializer = SPUImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = request.FILES.get('image')

        fdfs = FastDFSStorage()
        file_id = fdfs.save(image.name, image)

        img_url = fdfs.url(file_id)

        return Response({
            'img_url': img_url
        })


# GET /meiduo_admin/goods/brands/simple/
class BrandView(ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    pagination_class = None
