from ast import Or
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from product.models import Variation
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from utils import utils
from .models import Order, OrderItem

# Create your views here.


class DispatchLoginRequired(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:create')
        return super().dispatch(*args, **kwargs)


class Pay(DispatchLoginRequired, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, *args, **kwargs):
        return HttpResponse('Pay')


class SaveOrder(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You need to login.')
            return redirect('profiles:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Empty cart.')
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_id = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product').filter(id__in=cart_variation_id))

        for variation in bd_variations:
            vid = str(variation.id)
            stock = variation.stock
            qtt_cart = cart[vid]['quantity']
            unit_price = cart[vid]['unit_price']
            promotional_unit_price = cart[vid]['promotional_unit_price']

            error_stock = ''

            if stock < qtt_cart:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unit_price
                cart[vid]['promotional_quantitative_price'] = stock * \
                    promotional_unit_price

                error_stock = 'Your cart contains products that are out of stock. \
                      Please verify on your cart which products are affected by it.'

            total_qtt_cart = utils.total_cart_qtt(cart)
            total_price_cart = utils.cart_total_price(cart)

            if error_stock:
                messages.error(
                    self.request, error_stock)
                self.request.session.save()
                return redirect('product:cart')

            order = Order(
                user=self.request.user,
                total=total_price_cart,
                total_qtt=total_qtt_cart,
                stats='C',
            )

            order.save()

            # Instead of saving each instance separately, bulk_create performs \
            # a batch insert into the database, reducing the number of queries executed. \
            # It's particularly useful when you have a large number of objects to create, as it can \
            # significantly improve performance compared to saving them one by one.

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
            # return render(self.request, self.template_name)
            return redirect(
                reverse(
                    'order:pay',
                    kwargs={
                        'pk': order.pk
                    }
                )
            )


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')


class List(View):
    def get(self, *args, **kwargs):
        return HttpResponse('List')
