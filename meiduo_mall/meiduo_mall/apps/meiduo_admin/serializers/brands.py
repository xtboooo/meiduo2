from rest_framework import serializers

from goods.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """品牌序列化器类"""

    class Meta:
        model = Brand
        exclude = ('create_time', 'update_time')
