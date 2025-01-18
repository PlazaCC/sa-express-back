from decimal import Decimal

def quantize(value):
    return value.quantize(Decimal('1.000000'))