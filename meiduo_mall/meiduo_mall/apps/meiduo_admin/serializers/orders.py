from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderListSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')


class SKUGoodSerializer(serializers.ModelSerializer):
    """订单sku序列化器类"""

    class Meta:
        model = SKU
        fields = ('name', 'default_image')


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器类"""
    sku = SKUGoodSerializer(label='订单sku商品信息', read_only=True)

    class Meta:
        model = OrderGoods
        fields = ('count', 'price', 'sku')


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    user = serializers.StringRelatedField(label='下单用户', read_only=True)
    skus = OrderDetailSerializer(label='下单商品详情', many=True, read_only=True)

    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        exclude = ('update_time', 'address')


class OrderStatusSerializer(serializers.ModelSerializer):
    """订单状态序列化器类"""

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')
        # 元组只有一个值的时候必须要加逗号
        read_only_fields = ('order_id',)

    def update(self, instance, validated_data):
        """修改订单状态"""
        status = validated_data['status']

        instance.status = status
        instance.save()
        return instance
