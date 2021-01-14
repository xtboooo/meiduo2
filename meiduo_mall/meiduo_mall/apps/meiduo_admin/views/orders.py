from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

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

    # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/ -> status
    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        order = self.get_object()
        status = request.data.get('status')
        try:
            status = int(status)
        except:
            return Response({'message': 'status必须为整数'}, status=400)

        if status not in list(range(1, 7)):
            return Response({'message': 'status参数范围必须为1~6'}, status=400)

        order.status = status
        order.save()

        serializer = self.get_serializer(order)
        return Response({
            'order_id': order.order_id,
            'status': status
        })
