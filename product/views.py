from django.shortcuts import render, redirect, reverse, get_object_or_404  # type:ignore
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from . import models
# Create your views here.


class ProductList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):

        # if self.request.session.get('cart'):
        #     del self.request.session['cart']
        #     self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'This product does not exist.'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_stock = variation.stock
        product = variation.product

        product_id = product.pk
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        promotional_unit_price = variation.promotional_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(
                self.request, 'Insufficient stock'
            )
            return redirect(http_referer)

        # this 'if' statement check if a cart exists in a client account
        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']
        if variation_id in cart:
            # variation exists in the cart
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1

            if variation_stock < cart_quantity:
                messages.warning(
                    self.request, f'Insufficient stock for {cart_quantity}x in {product_name}.'
                    f'We add {variation_stock}x on your cart.'
                )
                cart_quantity = variation_stock

            cart[variation_id]['quantity'] = cart_quantity
            cart[variation_id]['quantitative_price'] = unit_price * cart_quantity
            cart[variation_id]['promotional_quantitative_price'] = promotional_unit_price * cart_quantity
        else:
            # variation does not exist in the cart
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quantitative_price': unit_price,
                'promotional_quantitative_price': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        return HttpResponse()


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')
