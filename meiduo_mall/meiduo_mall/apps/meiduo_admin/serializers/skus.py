from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification


class SKUImageSerializer(serializers.ModelSerializer):
    sku = serializers.StringRelatedField(label='SKU 商品名称')
    sku_id = serializers.IntegerField(label='SKU 商品id')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        """针对 sku_id 进行补充验证"""
        # SKU商品是否存在
        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('SKU商品不存在')
        return value

    def create(self, validated_data):
        """上传 SKU 商品图片保存"""
        # 调用 ModelSerializer 中的 create 方法，进行上传文件保存和表记录添加
        sku_image = super().create(validated_data)

        # 判断是否需要设置 SKU 商品的默认图片
        sku = sku_image.sku

        if not sku.default_image:
            sku.default_image = sku_image
            sku.save()
        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    """sku规格序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """sku商品序列化器类"""

    spu_id = serializers.IntegerField(label='商品spu id')
    category = serializers.StringRelatedField(label='所属第三级分类名称', )
    specs = SKUSpecSerializer(label='sku规格选项', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'comments', 'default_image', 'spu')
