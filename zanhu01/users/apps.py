from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "zanhu01.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import zanhu01.users.signals  # noqa F401
        except ImportError:
            pass
