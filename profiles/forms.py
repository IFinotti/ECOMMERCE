from django import forms
from pkg_resources import require
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    # to hide the password on the form

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'password',
            'email',
        )

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)
