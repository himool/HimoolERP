from decimal import Decimal


def plus(*args):
    """加"""
    return float(round(sum(map(lambda value: Decimal(str(value)), args)), 2))


def minus(*args):
    """减"""
    return float(round(sum(map(lambda value: -Decimal(str(value)), args[1:]), Decimal(str(args[0]))), 2))


def times(*args):
    """乘"""
    result = 1
    for value in args:
        result *= Decimal(str(value))
    return float(round(result, 2))


def divide(*args):
    """除"""
    result = Decimal(str(args[0]))
    for value in args[1:]:
        result /= Decimal(str(value)) if Decimal(str(value)) != 0 else Decimal(str('1'))
    return float(round(result, 2))
