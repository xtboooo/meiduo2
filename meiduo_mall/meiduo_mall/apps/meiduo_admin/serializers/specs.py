from rest_framework import serializers

from goods.models import SPUSpecification


class SpecSerializer(serializers.ModelSerializer):
    """商品规格序列化器类"""

    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time')