"""
Standard django apps module for the authentication core.
The authentication core module will handle the logging,
base model definition and session based authentication.
"""
from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Standard django app config for registering the core app.
    """

    name='bdreform.encauth.core'
    label='encauth_core'
    verbose_name = _('Authentication Core')
