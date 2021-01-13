from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(serializers.ModelSerializer):
    """频道序列化器类"""
    category = serializers.StringRelatedField(label='一级分类名')
    category_id = serializers.IntegerField(label='一级分类id')
    group = serializers.StringRelatedField(label='频道组名')
    group_id = serializers.IntegerField(label='频道组id')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')


class ChannelTypeSerializer(serializers.ModelSerializer):
    """频道组序列化器类"""

    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class Category123Serializer(serializers.ModelSerializer):
    """一二三级分类序列化器类"""

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')
