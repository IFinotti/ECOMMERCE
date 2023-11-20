from django import forms
from pkg_resources import require
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    # to hide the password on the form

    password2 = forms.CharField(
        required=False, widget=forms.PasswordInput(), label='Confirm password')

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
            'password2',
            'email',
        )

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}
        user_data = cleaned.get('username')
        password_data = cleaned.get('password')
        email_data = cleaned.get('email')

        user_db = User.objects.filter(username=user_data).first()

        if self.user:
            pass
        else:
            pass

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        exclude = ('user',)
