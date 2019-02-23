# Django
from django import forms
from django.contrib import auth
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import ValidationError

from administrator.models import Administrator
from volunteer.models import Volunteer


class AuthenticationForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        """
        informs user that his email is invalid during Password Reset

        :return: email of user
        :raises: ValidationError
        """
        email = self.cleaned_data['email']
        if not (
            Administrator.objects.filter(email__iexact=email).exists() or
            Volunteer.objects.filter(email__iexact=email).exists()
        ):
            raise ValidationError(
                "There is no user registered with "
                "the specified email address!"
            )
        return email


class ValidatingPasswordChangeForm(auth.forms.PasswordChangeForm):

    def clean_new_password1(self):
        password1 = self.cleaned_data['new_password1']
        checks = dict()
        checks['lower'] = any(char.islower() for char in password1)
        checks['digit'] = any(char.isdigit() for char in password1)
        checks['size'] = 6 <= len(password1)
        y = '[~!@#$%^&*()_+{}":;\']+$'
        checks['special'] = set(y).intersection(password1)
        if all(checks.values()):
            return password1
        else:
            raise ValidationError(
                "New password must have at least 6 characters, one "
                "lowercase letter, one "
                "special character and one digit.")