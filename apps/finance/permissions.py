from extensions.permissions import ModelPermission


class PaymentOrderPermission(ModelPermission):
    code = 'payment_order'


class CollectionOrderPermission(ModelPermission):
    code = 'collection_order'


class ChargeOrderPermission(ModelPermission):
    code = 'charge_order'


class AccountTransferRecordPermission(ModelPermission):
    code = 'account_transfer_record'


__all__ = [
    'PaymentOrderPermission', 'CollectionOrderPermission',
    'ChargeOrderPermission', 'AccountTransferRecordPermission',
]
