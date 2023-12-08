from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from product.models import Variation
from django.contrib import messages
from django.views import View

# Create your views here.


class Pay(View):
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
            Variation.objects.filter(id__in=cart_variation_id))
        context = {}
        return redirect(self.request, self.template_name, context)


class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FinishOrder')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')
