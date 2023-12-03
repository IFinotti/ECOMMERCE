from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from . import models
from . import forms
import copy
# Create your views here.


class ProfileBase(View):
    template_name = 'profiles/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))
        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Profile.objects.filter(
                user=self.request.user).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),

                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'profileform': forms.ProfileForm(data=self.request.POST or None)
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'
        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(ProfileBase):
    def post(self, *args, **kwargs):
        # if not self.userform.is_valid():
        if not self.userform.is_valid() or not self.profileform.is_valid():
            messages.error(
                self.request, "There's some errors in your register. Check that the fields have been filled correctly.")
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # user logged in
        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)
            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.Profile(**self.profileform.cleaned_data)
                profile.save()
            else:
                self.profileform.save(commit=False)
                profile.user = user
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            authentic = authenticate(
                self.request, username=user, password=password)

            if authentic:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(
            self.request, 'Your details are created/updated successfully')
        return redirect('product:cart')


class Update(View):
    def get(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(
                self.request, 'Invalid user or passwords')

            return redirect('profile:create')

        user = authenticate(self.request, username=username, password=password)

        if not user:
            messages.error(
                self.request, 'Invalid user or passwords')
            return redirect('profile:create')

        login(self.request, user=user)
        messages.success(
            self.request, 'You have succesfully logged in')
        return redirect('product:cart')


class Login(View):
    def post(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))
        logout(self.request)
        self.request.session['cart'] = cart
        self.request.session.save()
        return redirect('product:list')
