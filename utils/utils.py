def format_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def total_cart_qtt(cart):
    return sum([item['quantity'] for item in cart.values()])
