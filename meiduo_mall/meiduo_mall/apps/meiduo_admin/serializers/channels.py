import re

from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class ChannelSerializer(serializers.ModelSerializer):
    """频道序列化器类"""
    category = serializers.StringRelatedField(label='一级分类名', read_only=True)
    category_id = serializers.IntegerField(label='一级分类id')
    group = serializers.StringRelatedField(label='频道组名', read_only=True)
    group_id = serializers.IntegerField(label='频道组id')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')

    def validate(self, attrs):
        category_id = attrs['category_id']
        group_id = attrs['group_id']
        sequence = attrs['sequence']
        url = attrs['url']

        try:
            channel_group = GoodsChannelGroup.objects.get(id=group_id)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组id参数有误')

        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('分类id参数有误')

        if not re.match(r'((http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)'
                        r'+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)', url):
            raise serializers.ValidationError('url参数有误')

        # sequence展示顺序重复??
        if sequence <= 0:
            raise serializers.ValidationError('sequence参数有误')

        return attrs


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
