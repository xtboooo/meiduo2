from rest_framework import serializers

from goods.models import SPU, Brand


class SPUSerializer(serializers.ModelSerializer):
    brand = serializers.StringRelatedField(label='品牌名称')
    brand_id = serializers.IntegerField(label='品牌id')
    category1_id = serializers.IntegerField(label='一级分类id')
    category2_id = serializers.IntegerField(label='二级分类id')
    category3_id = serializers.IntegerField(label='三级分类id')

    class Meta:
        model = SPU
        exclude = ('create_time', 'update_time', 'category1', 'category2', 'category3')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name')
