from extensions.permissions import InterfacePermission


class PaymentOrderPermission(InterfacePermission):
    code = 'payment_order'


class CollectionOrderPermission(InterfacePermission):
    code = 'collection_order'


class ChargeOrderPermission(InterfacePermission):
    code = 'charge_order'


class AccountTransferRecordPermission(InterfacePermission):
    code = 'account_transfer_record'


__all__ = [
    'PaymentOrderPermission', 'CollectionOrderPermission',
    'ChargeOrderPermission', 'AccountTransferRecordPermission',
]
