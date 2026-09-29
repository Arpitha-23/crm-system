
from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def manager_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        # Superusers are always allowed
        if request.user.is_superuser:
            return view_func(
                request,
                *args,
                **kwargs
            )

        # Managers are allowed
        if request.user.groups.filter(
            name='Managers'
        ).exists():

            return view_func(
                request,
                *args,
                **kwargs
            )

        # Everyone else is denied
        messages.error(
            request,
            'You do not have permission to access this page.'
        )

        return redirect(
            'dashboard'
        )

    return wrapper

