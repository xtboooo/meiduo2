from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class SKUGoodSerializer(serializers.ModelSerializer):
    """订单sku序列化器类"""

    class Meta:
        model = SKU
        fields = ('id', 'name', 'default_image')


class OrderDetailSerializer(serializers.ModelSerializer):
    """订单详情序列化器类"""
    sku = SKUGoodSerializer(label='订单sku商品信息', read_only=True)

    class Meta:
        model = OrderGoods
        fields = ('id', 'count', 'price', 'sku')


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器类"""
    user = serializers.StringRelatedField(label='下单用户', read_only=True)
    skus = OrderDetailSerializer(label='下单商品详情', many=True, read_only=True)

    class Meta:
        model = OrderInfo
        exclude = ('update_time', 'address')

