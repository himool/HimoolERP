from extensions.models import *


class StockInOrder(Model):
    """入库单据"""

    class Type(TextChoices):
        """入库类型"""

        PURCHASE = ('purchase', '采购')
        SALES_RETURN = ('sales_return', '销售退货')

    number = CharField(max_length=32, verbose_name='编号')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='stock_in_orders', verbose_name='仓库')
    type = CharField(max_length=32, choices=Type.choices, verbose_name='入库类型')
    purchase_order = OneToOneField('purchase.PurchaseOrder', on_delete=CASCADE, null=True,
                                   related_name='stock_in_order', verbose_name='采购单据')
    sales_return_order = OneToOneField('sales.SalesReturnOrder', on_delete=CASCADE, null=True,
                                       related_name='stock_in_order', verbose_name='销售退货单据')
    total_quantity = FloatField(verbose_name='入库总数')
    remain_quantity = FloatField(default=0, verbose_name='入库剩余数量')
    is_completed = BooleanField(default=False, verbose_name='完成状态')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_orders')

    class Meta:
        unique_together = [('number', 'team')]

    @classmethod
    def get_number(cls, team):
        start_date, end_date = get_today(), get_tomorrow()
        instance = cls.objects.filter(team=team, create_time__gte=start_date, create_time__lt=end_date).last()

        try:
            result = re.match('^(.*?)([1-9]+)$', instance.number)
            number = result.group(1) + str(int(result.group(2)) + 1)
        except AttributeError:
            number = 'RK' + pendulum.today(settings.TIME_ZONE).format('YYYYMMDD') + '0001'

        return number

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.is_completed = self.remain_quantity == 0
        if update_fields:
            update_fields.append('is_completed')
        return super().save(force_insert, force_update, using, update_fields)


class StockInGoods(Model):
    """入库商品"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_goods_set', verbose_name='入库单据')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='stock_in_goods_set', verbose_name='商品')
    stock_in_quantity = FloatField(verbose_name='入库总数')
    remain_quantity = FloatField(default=0, verbose_name='入库剩余数量')
    is_completed = BooleanField(default=False, verbose_name='完成状态')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_goods_set')

    class Meta:
        unique_together = [('stock_in_order', 'goods')]

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.is_completed = self.remain_quantity == 0
        if update_fields:
            update_fields.append('is_completed')
        return super().save(force_insert, force_update, using, update_fields)


class StockInRecord(Model):
    """入库记录"""

    stock_in_order = ForeignKey('stock_in.StockInOrder', on_delete=CASCADE,
                                related_name='stock_in_records', verbose_name='入库单据')
    warehouse = ForeignKey('data.Warehouse', on_delete=PROTECT, related_name='stock_in_records', verbose_name='仓库')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='stock_in_records', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_quantity = FloatField(verbose_name='入库总数')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_stock_in_records', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_records')


class StockInRecordGoods(Model):
    """入库记录商品"""

    stock_in_record = ForeignKey('stock_in.StockInRecord', on_delete=CASCADE,
                                 related_name='stock_in_record_goods_set', verbose_name='入库记录')
    stock_in_goods = ForeignKey('stock_in.StockInGoods', on_delete=CASCADE,
                                related_name='stock_in_record_goods_set', verbose_name='入库商品')
    goods = ForeignKey('goods.Goods', on_delete=PROTECT, related_name='stock_in_record_goods_set', verbose_name='商品')
    stock_in_quantity = FloatField(default=0, verbose_name='入库数量')
    enable_batch_control = BooleanField(default=False, verbose_name='启用批次控制')
    production_date = DateField(null=True, verbose_name='生产日期')
    shelf_life_days = IntegerField(default=0, verbose_name='保质期天数')
    expiration_date = DateField(null=True, verbose_name='过期日期')
    batch = OneToOneField('goods.Batch', on_delete=CASCADE, null=True,
                          related_name='stock_in_record_goods', verbose_name='批次')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='stock_in_record_goods_set')

    class Meta:
        unique_together = [('stock_in_record', 'goods')]


__all__ = [
    'StockInOrder', 'StockInGoods',
    'StockInRecord', 'StockInRecordGoods',
]
