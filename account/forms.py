import email
from django import forms
from pkg_resources import require
from . import models
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
    )
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
        password2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'User already exists'
        error_msg_email_exists = 'E-mail already exists'
        error_msg_password_match = 'The passwords are not the same'
        error_msg_short_password = 'E-mail already exists'
        error_msg_required_field = 'This field is required'

        if self.user:
            if user_db:
                if user_data != user_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password2_data) < 8:
                    validation_error_msgs['password'] = error_msg_short_password

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

        else:
            if user_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password2_data) < 8:
                validation_error_msgs['password'] = error_msg_short_password

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

        if validation_error_msgs:
            raise (forms.ValidationError(validation_error_msgs))


class AccountForm(forms.ModelForm):
    class Meta:
        model = models.Account
        fields = '__all__'
        exclude = ('user',)
