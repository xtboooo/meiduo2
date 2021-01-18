from django.db import transaction
from django.db import DatabaseError
from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, SPU, SPUSpecification, SpecificationOption


class SKUImageSerializer(serializers.ModelSerializer):
    sku = serializers.StringRelatedField(label='SKU 商品名称')
    sku_id = serializers.IntegerField(label='SKU 商品id')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')

    def validate_sku_id(self, value):
        """针对 sku_id 进行补充验证"""
        # SKU商品是否存在
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('SKU商品不存在')
        return value

    def create(self, validated_data):
        """上传 SKU 商品图片保存"""
        # 调用 ModelSerializer 中的 create 方法，进行上传文件保存和表记录添加
        sku_image = super().create(validated_data)

        # 判断是否需要设置 SKU 商品的默认图片
        sku = sku_image.sku

        if not sku.default_image:
            sku.default_image = sku_image
            sku.save()
        return sku_image


class SKUSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    """sku规格序列化器类"""
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """sku商品序列化器类"""

    spu_id = serializers.IntegerField(label='商品spu id')
    category = serializers.StringRelatedField(label='所属第三级分类名称', read_only=True)
    specs = SKUSpecSerializer(label='sku规格选项', many=True)

    class Meta:
        model = SKU
        exclude = ('create_time', 'update_time', 'comments', 'default_image', 'spu')
        extra_kwargs = {
            'sales': {
                'read_only': True
            }
        }

    def validate(self, attrs):
        # 1.校验spu_id
        spu_id = attrs.get('spu_id')
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('spu_id参数有误')
        # 关键点 请求中没有三级分类id,但是在新增sku商品时改参数是必填的,所以在这里要补充进去
        attrs['category_id'] = spu.category3_id

        # 2.校验规格数据(数量+数据一致性)
        specs = attrs.get('specs')  # specs是list

        # 数量检查
        specs_count = len(specs)
        spu_specs_count = spu.specs.count()
        if specs_count != spu_specs_count:
            raise serializers.ValidationError('规格数据数量有误')

        # 数据是否一致
        spec_ids = [spec.get('spec_id') for spec in specs]
        spu_spec_ids = [spec.id for spec in spu.specs.all()]

        # 排序检查
        if spec_ids.sort() != spu_spec_ids.sort():
            raise serializers.ValidationError('规格数据参数有误')

        # 3.校验选项参数
        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')
            # 获取spec_id对应规格下的选项
            options = SpecificationOption.objects.filter(spec_id=spec_id)
            option_ids = [option.id for option in options]
            if option_id not in option_ids:
                raise serializers.ValidationError('选项参数有误')
        return attrs

    def create(self, validated_data):
        # self指的是当前序列化器对象，在self下面有个context属性保存了请求对象
        # specs = self.context['request'].data.get('specs')
        specs = validated_data.get('specs')

        del validated_data['specs']
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                # sku = SKU.objects.create(**validated_data)
                sku = super().create(validated_data)
                for spec in specs:
                    spec_id = spec['spec_id']
                    option_id = spec['option_id']
                    SKUSpecification.objects.create(sku=sku, spec_id=spec_id, option_id=option_id)
            except Exception as e:
                transaction.savepoint_rollback(sid)
                raise DatabaseError('数据库保存错误')
            else:
                transaction.savepoint_commit(sid)
                return sku

    def update(self, instance, validated_data):
        specs = validated_data.pop('specs')
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                super().update(instance, validated_data)
                instance.specs.all().delete()

                for spec in specs:
                    SKUSpecification.objects.create(
                        sku_id=instance.id,
                        spec_id=spec['spec_id'],
                        option_id=spec['option_id']
                    )
            except Exception:
                transaction.savepoint_rollback(sid)
                raise DatabaseError('数据保存出错')
            else:
                transaction.savepoint_commit(sid)
                return instance


class SPUSimpleSerializer(serializers.ModelSerializer):
    """spu商品简单信息系列化棋类"""

    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptSerializer(serializers.ModelSerializer):
    """spu商品选项序列化器类"""

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')
        extra_kwargs = {
            'value': {
                'read_only': True
            }
        }


class SPUSpecSerializer(serializers.ModelSerializer):
    """spu商品规格序列化器类"""
    options = SpecOptSerializer(label='选项', read_only=True, many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'options')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }
