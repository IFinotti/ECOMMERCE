def format_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def total_cart_qtt(cart):
    return sum([item['quantity'] for item in cart.values()])


def cart_totals(cart):
    total = 0
    for item in cart.values():
        # Garantindo que a quantidade seja obtida corretamente
        quantity = item.get('quantity', 1)
        unit_price = item.get('promotional_unit_price') if item.get(
            'promotional_unit_price') else item.get('unit_price')
        # Multiplica o preço unitário pela quantidade correta de cada item
        total += quantity * unit_price
    return total
