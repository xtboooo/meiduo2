from rest_framework import serializers

from goods.models import SPU, Brand, GoodsCategory


class SPUSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(label='品牌名称')
    brand_id = serializers.IntegerField(label='品牌id')
    category1_id = serializers.IntegerField(label='一级分类id')
    category2_id = serializers.IntegerField(label='二级分类id')
    category3_id = serializers.IntegerField(label='三级分类id')

    extra_kwargs = {
        'sales': {
            'read_only': True
        },
        'comments': {
            'read_only': True
        }
    }

    class Meta:
        model = SPU
        exclude = ('create_time', 'update_time', 'category1', 'category2', 'category3')

    def validate(self, attrs):
        brand_id = attrs.get('brand_id')
        category1_id = attrs.get('category1_id')
        category2_id = attrs.get('category2_id')
        category3_id = attrs.get('category3_id')
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError('brand_id参数有误')

        try:
            category1 = GoodsCategory.objects.get(id=category1_id, parent_id=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('category1_id参数有误')

        try:
            category2 = GoodsCategory.objects.get(id=category2_id, parent_id__in=list(range(1, 38)))
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('category2_id参数有误')

        try:
            category3 = GoodsCategory.objects.get(id=category3_id, parent_id__in=list(range(38, 115)))
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('category3_id参数有误')

        return attrs


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')


class SPUImageSerializer(serializers.Serializer):
    image = serializers.ImageField(label='spu图片', write_only=True)
