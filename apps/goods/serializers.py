from rest_framework import serializers
from .models import Goods, Category


class CategorySerializer(serializers.ModelSerializer):
    goods_count = serializers.SerializerMethodField('get_goods_count')

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'order', 'goods_count']
        read_only_fields = ['id', 'goods_count']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError
        return data

    def get_goods_count(self, obj):
        return obj.goods.all().count()


class GoodsSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Goods
        fields = ['id', 'name', 'code', 'specification', 'unit', 'brand', 'category', 'category_name',
                  'purchase_price', 'suggested_retail_price', 'retail_price', 'inventory_warning_lower_limit',
                  'inventory_warning_upper_limit', 'initial_quantity', 'order', 'status']
        read_only_fields = ['id', 'category_name']

    def validate(self, data):
        if not data.get('name') or not data.get('code'):
            raise serializers.ValidationError

        if data.get('purchase_price') is None or data.get('retail_price') is None:
            raise serializers.ValidationError

        # 商品分类
        teams = self.context['request'].user.teams
        if data['category'] and data['category'].id not in teams.category_set.all().values_list('id', flat=True):
            raise serializers.ValidationError

        return data

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
