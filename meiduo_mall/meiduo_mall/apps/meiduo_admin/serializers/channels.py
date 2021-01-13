from rest_framework import serializers

from goods.models import GoodsChannel


class ChannelSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(label='一级分类名')
    category_id = serializers.IntegerField(label='一级分类id')
    group = serializers.StringRelatedField(label='频道组名')
    group_id = serializers.IntegerField(label='频道组id')

    class Meta:
        model = GoodsChannel
        exclude = ('create_time', 'update_time')
