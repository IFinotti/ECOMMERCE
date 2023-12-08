from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib import messages
from django.views import View

# Create your views here.


class Pay(View):
    template_name = 'order/pay.html'

    def get(self, *args, **kwargs):
        context = {}
        return redirect(self.request, self.template_name, context)


class SaveOrder(View):
    def get(self, *args, **kwargs):
        return HttpResponse('FinishOrder')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detail')
