from re import U
from django.template import Library
from utils import utils

register = Library()


@register.filter
def format_price(val):
    return utils.format_price(val)


def total_cart_qtt(cart):
    return utils.total_cart_qtt(cart)
