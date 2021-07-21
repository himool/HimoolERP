from .models import SalesOrder, SalesTask, Client, PaymentRecord
from rest_framework import serializers
from django.db.models import Sum, F
from warehouse.models import Flow
import re


class SalesOrderSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'seller_username', 'warehouse_name', 'account_name', 'is_done',
                            'goods_set', 'total_amount']
        fields = ['date', 'seller', 'warehouse', 'account', 'discount', 'amount', 'client_phone',
                  'client_contacts', 'client_name', 'client_address', 'remark', 'is_return',
                  'sales_order', *read_only_fields]

    def validate(self, data):
        if not data.get('seller') or not data.get('warehouse') or not data.get('account'):
            raise serializers.ValidationError

        if data.get('amount') is None or not data.get('date'):
            raise serializers.ValidationError

        if data.get('discount') is None or data['discount'] <= 0:
            raise serializers.ValidationError

        client_phone = data.get('client_phone')
        if client_phone and not re.match(r'^1[3456789]\d{9}$', client_phone):
            raise serializers.ValidationError

        # 验证修改销售员权利
        if self.context['request'].user.username != data['seller']:
            user_roles = self.context['request'].user.roles.all()
            permissions = sum(user_roles.values_list('permissions', flat=True), [])
            if user_roles.count() != 0 and 'CHANGE_SELLER' not in permissions:
                raise serializers.ValidationError

        # goods_set
        goods_set = self.context['request'].data.get('goods_set', [])
        if not goods_set:
            raise serializers.ValidationError

        for item in goods_set:
            if item.get('id') is None or item.get('retail_price') is None:
                raise serializers.ValidationError

            if not item.get('quantity') or item['quantity'] <= 0:
                raise serializers.ValidationError

        # 退货单
        if data.get('is_return', False) and not data.get('sales_order'):
            raise serializers.ValidationError

        return data

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'code', 'name', 'specification', 'unit', 'quantity',
                                          'retail_price', 'amount', 'remark')


class SalesPaymentRecordSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField('get_client_name')

    class Meta:
        model = PaymentRecord
        read_only_fields = ['sales_order', 'date', 'amount',  'remark', 'client_name']
        fields = [*read_only_fields]

    def get_client_name(self, obj):
        return obj.sales_order.client_name


class SalesOrderProfitSerializer(serializers.ModelSerializer):
    goods_set = serializers.SerializerMethodField('get_goods_set')

    class Meta:
        model = SalesOrder
        read_only_fields = ['id', 'date', 'warehouse',  'warehouse_name', 'discount', 'goods_set']
        fields = [*read_only_fields]

    def get_goods_set(self, obj):
        return obj.goods_set.all().values('id', 'code', 'name', 'specification', 'unit', 'quantity',
                                          'retail_price', 'purchase_price', 'remark')


class SalesTaskSerializer(serializers.ModelSerializer):
    goods_name = serializers.SerializerMethodField('get_goods_name')
    warehouse_name = serializers.SerializerMethodField('get_warehouse_name')
    completed_quantity = serializers.SerializerMethodField('get_completed_quantity')

    class Meta:
        model = SalesTask
        fields = ['id', 'goods', 'goods_name', 'warehouse', 'warehouse_name', 'quantity',
                  'start_date', 'end_date', 'create_date', 'completed_quantity']
        read_only_fields = ['id', 'goods_name', 'warehouse_name', 'create_date', 'completed_quantity']

    def validate(self, data):
        if not data.get('goods') or not data.get('warehouse') or data.get('quantity') is None:
            raise serializers.ValidationError

        if not data.get('start_date') or not data.get('end_date'):
            raise serializers.ValidationError

        teams = self.context['request'].user.teams
        if data['goods'].teams != teams or data['warehouse'].teams != teams:
            raise serializers.ValidationError

        return data

    def get_goods_name(self, obj):
        return obj.goods.name

    def get_warehouse_name(self, obj):
        return obj.warehouse.name

    def get_completed_quantity(self, obj):
        result = Flow.objects.filter(teams=obj.teams, goods=obj.goods, warehouse=obj.warehouse, create_datetime__gte=obj.start_date,
                                     create_datetime__lte=obj.end_date, sales_order__isnull=False).aggregate(total=Sum('change_quantity'))
        return -result['total'] if result['total'] else 0


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'name', 'address', 'mailbox', 'create_date', 'contacts']
        read_only_fields = ['id', 'create_date']

    def validate(self, data):
        if not data.get('phone'):
            raise serializers.ValidationError
        return data
