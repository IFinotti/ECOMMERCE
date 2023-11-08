from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models
# Create your views here.


class ProductList(ListView):
    model = models.Product
    template_name = 'product/list.html'


class ProductDetail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('ProductDetail')


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('AddToCart')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('RemoveFromCart')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Cart')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finish')
