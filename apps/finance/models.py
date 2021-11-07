from extensions.models import *


class PaymentOrder(Model):
    """付款单据"""

    number = CharField(max_length=32, verbose_name='编号')
    supplier = ForeignKey('data.Supplier', on_delete=PROTECT, related_name='payment_orders', verbose_name='供应商')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='payment_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(null=True, verbose_name='总金额')
    discount_amount = AmountField(default=0, verbose_name='优惠金额')
    payment_amount = AmountField(null=True, verbose_name='实付金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_payment_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='payment_orders')

    class Meta:
        unique_together = [('number', 'team')]


class PaymentAccount(Model):
    """付款账户"""

    payment_order = ForeignKey('finance.PaymentOrder', on_delete=CASCADE,
                               related_name='payment_accounts', verbose_name='付款单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='payment_accounts', verbose_name='结算账户')
    payment_amount = AmountField(verbose_name='付款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='payment_accounts')

    class Meta:
        unique_together = [('patment_order', 'account')]


class CollectionOrder(Model):
    """收款单据"""

    number = CharField(max_length=32, verbose_name='编号')
    client = ForeignKey('data.Client', on_delete=PROTECT, related_name='collection_orders', verbose_name='客户')
    handler = ForeignKey('system.User', on_delete=PROTECT, related_name='collection_orders', verbose_name='经手人')
    handle_time = DateTimeField(verbose_name='处理时间')
    remark = CharField(max_length=256, null=True, blank=True, verbose_name='备注')
    total_amount = AmountField(null=True, verbose_name='总金额')
    discount_amount = AmountField(default=0, verbose_name='优惠金额')
    collection_amount = AmountField(null=True, verbose_name='实收金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    creator = ForeignKey('system.User', on_delete=PROTECT,
                         related_name='created_collection_orders', verbose_name='创建人')
    create_time = DateTimeField(auto_now_add=True, verbose_name='创建时间')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='collection_orders')

    class Meta:
        unique_together = [('number', 'team')]


class CollectionAccount(Model):
    """收款账户"""

    collection_order = ForeignKey('finance.CollectionOrder', on_delete=CASCADE,
                                  related_name='collection_accounts', verbose_name='收款单据')
    account = ForeignKey('data.Account', on_delete=PROTECT, related_name='collection_accounts', verbose_name='结算账户')
    collection_amount = AmountField(verbose_name='付款金额')
    is_void = BooleanField(default=False, verbose_name='作废状态')
    team = ForeignKey('system.Team', on_delete=CASCADE, related_name='collection_accounts')

    class Meta:
        unique_together = [('collection_order', 'account')]


class ChargeRecord(Model):
    """收支记录"""


class AccountTransferRecord(Model):
    """结算账户转账记录"""


__all__ = [

]
