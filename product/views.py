from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
# Create your views here.


class ProductList(ListView):
    ...


class ProductDetail(View):
    ...


class AddToCart(View):
    ...


class RemoveFromCart(View):
    ...


class Cart(View):
    ...


class Finish(View):
    ...
