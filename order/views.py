from django.views.generic import DetailView
from django.shortcuts import redirect
from django.shortcuts import redirect, reverse, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views import View
# from django.http import HttpResponse
from .mp import create_payment_preference
from django.contrib import messages

from product.models import Variation, Product
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


class Success(DetailView):
    template_name = 'order/success.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Verifica se o status já foi aprovado para evitar duplicidade
        if self.object.status != 'A':
            # Atualiza o status da ordem para 'Aprovado'
            self.object.status = 'A'
            self.object.save()

            # Atualiza o estoque dos produtos associados à ordem
            for item in self.object.orderitem_set.all():
                try:
                    # Busque a variação correta usando o variation_id
                    variation = Variation.objects.get(id=item.variation_id)
                    variation.stock -= item.quantity  # Subtrai a quantidade comprada
                    variation.save()
                except Variation.DoesNotExist:
                    # Lida com o caso de não encontrar uma variação vinculada
                    messages.error(
                        request, 'Erro ao atualizar o estoque. Variação não encontrada.')
                    return redirect('order:failure', pk=self.object.pk)

        # Redireciona para a página de sucesso
        return super().get(request, *args, **kwargs)


class Failure(DetailView):
    template_name = 'order/failure.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Atualiza o status da ordem para 'Disapproved'
        self.object.status = 'D'
        self.object.save()

        return super().get(request, *args, **kwargs)


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        # Garante que o self.object seja definido
        self.object = self.get_object()

        # Gera o link de pagamento de forma dinâmica
        payment_link = create_payment_preference(self.object, request)
        if not payment_link:
            return redirect('error_page')

        # Adiciona o payment_link ao contexto
        context = self.get_context_data(payment_link=payment_link)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        # Obtém o contexto padrão da classe pai
        context = super().get_context_data(**kwargs)

        # Adiciona o payment_link ao contexto
        context['payment_link'] = kwargs.get('payment_link')
        return context


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

            error_msg_stock = ''

            if stock < cart_qtt:
                cart[vid]['quantity'] = stock
                error_msg_stock = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados.'

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
            status='P',
        )
        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=get_object_or_404(Product, id=v['product_id']),
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
                kwargs={'pk': order.pk}
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
