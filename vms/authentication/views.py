# Django
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView

# local Django
from vms import settings
from authentication.forms import ValidatingPasswordChangeForm


class ChangePasswordView(PasswordChangeView):
    form_class = ValidatingPasswordChangeForm


def index(request):
    return redirect(reverse('authentication:login_process'))


def anonymous_required(func):
    """
    Function for login and logout process using Django's built in auth-views
    """

    def as_view(request, *args, **kwargs):
        redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL)
        if request.user.is_authenticated():
            return redirect(redirect_to)
        response = func(request, *args, **kwargs)
        return response

    return as_view

