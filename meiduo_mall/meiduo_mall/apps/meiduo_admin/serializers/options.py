from rest_framework import serializers

from goods.models import SpecificationOption, SPUSpecification


class OptionSerializer(serializers.ModelSerializer):
    """规格选项序列化器类"""
    spec = serializers.StringRelatedField(label='规格名称', read_only=True)
    spec_id = serializers.IntegerField(label='规格id')

    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')

    def validate_spec_id(self, value):
        try:
            SPUSpecification.objects.get(id=value)
        except SpecificationOption.DoesNotExist:
            raise serializers.ValidationError('规格数据不存在')
        return value


class SpecSimpleSerializer(serializers.ModelSerializer):
    """简单规格序列化类"""

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')
