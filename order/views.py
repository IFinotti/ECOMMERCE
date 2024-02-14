from django.shortcuts import redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
# from django.http import HttpResponse
from django.contrib import messages

from product.models import Variation
from .models import Order, OrderItem

from utils import utils


class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login.'
            )
            return redirect('account:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product')
            .filter(id__in=cart_variation_ids)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            stock = variation.stock
            cart_qtt = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']

            error_msg_stock = ''

            if stock < cart_qtt:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unit_price
                cart[vid]['promotional_quantitative_price'] = stock * \
                    promotional_unit_price

                error_msg_stock = 'Estoque insuficiente para alguns '\
                    'produtos do seu cart. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_stock:
                messages.error(
                    self.request,
                    error_msg_stock
                )

                self.request.session.save()
                return redirect('product:cart')

        total_cart_qtt = utils.total_cart_qtt(cart)
        total_cart_price = utils.cart_totals(cart)

        order = Order(
            user=self.request.user,
            total=total_cart_price,
            total_qtt=total_cart_qtt,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promotional_price=v['promotional_quantitative_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']

        return redirect(
            reverse(
                'order:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'


class List(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 10
    ordering = ['-id']
