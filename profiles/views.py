from django.shortcuts import render
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponse
from . import models
from . import forms
# Create your views here.


class ProfileBase(View):
    template_name = 'profile/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.context = {
            'userform': forms.UserForm(data=self.request.POST or None),
            'profileform': forms.ProfileForm(data=self.request.POST or None)
        }

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(ProfileBase):
    pass


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Update')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')
