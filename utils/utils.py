def format_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def total_cart_qtt(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_totals(cart):
    return sum(
        [
            item.get('promotional_quantitative_price')
            if item.get('promotional_quantitative_price')
            else item.get('quantitative_price')
            for item
            in cart.values()
        ]
    )
