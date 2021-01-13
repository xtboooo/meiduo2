from rest_framework import serializers

from goods.models import SPUSpecification, SPU


class SpecSerializer(serializers.ModelSerializer):
    """商品规格序列化器类"""
    spu = serializers.StringRelatedField(label='spu商品名称', read_only=True)
    spu_id = serializers.IntegerField(label='spu商品id')

    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time')

    def validate_spu_id(self, value):
        try:
            spu = SPU.objects.get(id=value)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('spu_id参数有误')
        return value
