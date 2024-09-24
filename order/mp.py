import mercadopago
from django.urls import reverse
# import os
# from dotenv import load_dotenv

# load_dotenv()


def create_payment_preference(order, request):
    sdk = mercadopago.SDK(
        "APP_USR-7583888755221388-080319-687eb0d4ca445458928fe2cc798b0245-547624382")

    items = []
    for item in order.orderitem_set.all():
        product = item.product

        unit_price = item.promotional_price if item.promotional_price > 0 else item.price

        # Print para depuração
        print(f'Produto: {product.name}')
        print(f'  Preço promocional: {item.promotional_price}')
        print(f'  Preço normal: {item.price}')
        print(f'  Preço unitário usado: {unit_price}')
        print(f'  Quantidade: {item.quantity}')

        items.append({
            "id": product.id,
            "title": product.name,
            "description": product.shortest_description,
            "picture_url": product.image.url,
            "category_id": "category_id_placeholder",
            "quantity": item.quantity,
            "currency_id": "BRL",
            "unit_price": unit_price / item.quantity,
        })

    success_url = request.build_absolute_uri(
        reverse('order:success', args=[order.pk]))
    failure_url = request.build_absolute_uri(
        reverse('order:failure', args=[order.pk]))
    # pending_url = request.build_absolute_uri(
    #     reverse('order:pending', args=[order.pk]))

    request_data = {
        "items": items,
        "back_urls": {
            "success": success_url,
            "failure": failure_url,
            # "pending": pending_url,
        },
        "auto_return": "all",
    }

    # Print para depuração
    print('Itens para pagamento:')
    for item in items:
        print(f'  ID: {item["id"]}')
        print(f'  Título: {item["title"]}')
        print(f'  Quantidade: {item["quantity"]}')
        print(f'  Preço unitário: {item["unit_price"]}')

    preference_response = sdk.preference().create(request_data)
    preference = preference_response["response"]
    return preference['init_point']
