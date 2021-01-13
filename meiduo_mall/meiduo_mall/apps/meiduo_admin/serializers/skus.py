from rest_framework import serializers

from goods.models import SKUImage, SKU


class SKUImageSerializer(serializers.ModelSerializer):
    sku = serializers.StringRelatedField(label='SKU 商品名称')
    sku_id = serializers.IntegerField(label='SKU 商品id')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')


class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id', 'name')
