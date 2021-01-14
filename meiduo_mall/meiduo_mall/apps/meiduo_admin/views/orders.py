from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.orders import OrderSerializer
from orders.models import OrderInfo


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = OrderSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        if keyword == '' or keyword is None:
            return OrderInfo.objects.all()
        else:
            return OrderInfo.objects.filter(order_id__contains=keyword)