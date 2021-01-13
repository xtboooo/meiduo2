from rest_framework import serializers

from goods.models import SpecificationOption


class OptionSerializer(serializers.ModelSerializer):
    """规格选项序列化器类"""
    spec = serializers.StringRelatedField(label='规格名称', read_only=True)
    spec_id = serializers.IntegerField(label='规格id')

    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')