from django.db.models import CharField, DateField, DateTimeField, JSONField, FileField, ImageField
from django.db.models import BooleanField, IntegerField, FloatField, DecimalField
from django.db.models.deletion import CASCADE, SET_NULL, SET_DEFAULT, PROTECT
from django.db.models import OneToOneField, ForeignKey, ManyToManyField
from django.db.models import Model, IntegerChoices, TextChoices
from django.db.models import Sum, Count, Value, F, Q, Prefetch
from django.db.models.functions import Coalesce
from django.db import transaction, connection
from datetime import datetime, timezone
from django.conf import settings
import pendulum
import re


class AmountField(DecimalField):
    """金额字段"""

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['max_digits'], kwargs['decimal_places'] = 16, 2
        super().__init__(verbose_name, name, **kwargs)


def get_yesterday():
    """昨日"""

    time = pendulum.yesterday(settings.TIME_ZONE).to_datetime_string()
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').astimezone(tz=timezone.utc).replace(tzinfo=timezone.utc)
    return time


def get_today():
    """今日"""

    time = pendulum.today(settings.TIME_ZONE).to_datetime_string()
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').astimezone(tz=timezone.utc).replace(tzinfo=timezone.utc)
    return time


def get_tomorrow():
    """明日"""

    time = pendulum.tomorrow(settings.TIME_ZONE).to_datetime_string()
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S').astimezone(tz=timezone.utc).replace(tzinfo=timezone.utc)
    return time


__all__ = [
    'Model', 'IntegerChoices', 'TextChoices',
    'CASCADE', 'SET_NULL', 'SET_DEFAULT', 'PROTECT',
    'OneToOneField', 'ForeignKey', 'ManyToManyField',
    'BooleanField', 'IntegerField', 'FloatField', 'DecimalField', 'AmountField',
    'CharField', 'DateField', 'DateTimeField', 'JSONField', 'FileField', 'ImageField',
    'Sum', 'Count', 'Value', 'F', 'Q', 'Prefetch', 'Coalesce', 'transaction', 'connection',
    'pendulum', 're', 'settings', 'get_yesterday', 'get_today', 'get_tomorrow',
]
