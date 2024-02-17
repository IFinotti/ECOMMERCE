from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q

from . import models
from account.models import Account


class ProductList(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


class Search(ProductList):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(shortest_description__icontains=termo) |
            Q(longest_description__icontains=termo)
        )

        self.request.session.save()
        return qs


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=variation_id)
        variation_stock = variation.stock
        product = variation.product

        product_id = product.id
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
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variation_id in cart:
            cart_quantity = cart[variation_id]['quantity']
            cart_quantity += 1

            if variation_stock < cart_quantity:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {cart_quantity}x no '
                    f'produto "{product_name}". Adicionamos {variation_stock}x '
                    f'no seu carrinho.'
                )
                cart_quantity = variation_stock

            cart[variation_id]['quantidade'] = cart_quantity
            cart[variation_id]['preco_quantitativo'] = unit_price * \
                cart_quantity
            cart[variation_id]['preco_quantitativo_promocional'] = promotional_unit_price * \
                cart_quantity
        else:
            cart[variation_id] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': variation_id,
                'unit_price': unit_price,
                'promotional_unit_price': promotional_unit_price,
                'quantitative_price': unit_price,
                'promotional_quantitative_price': promotional_unit_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {product_name} {variation_name} adicionado ao seu '
            f'carrinho {cart[variation_id]["quantity"]}x.'
        )

        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER', reverse('product:list')
        )
        variation_id = self.request.GET.get('vid')

        if not variation_id:
            print('Variation ID not found')  # Debug
            return redirect(http_referer)

        if not variation_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variation_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variation_id]

        print('Before deletion')  # Adiciona este log

        messages.success(
            self.request, f'Product {cart["product_name"]} {cart["variation_name"]} removed from your cart')
        del self.request.session['cart'][variation_id]

        self.request.session.save()

        print('After deletion')  # Adiciona este log

        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart', {}),
        }

        return render(self.request, 'product/cart.html', context)


class PurchaseSummary(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('account:create')

        account = Account.objects.filter(user=self.request.user).exists()

        if not account:
            messages.error(self.request, 'User does not have a profile.')
            return redirect('account:create')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Empty cart.')

            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'product/purchasesummary.html', context)
