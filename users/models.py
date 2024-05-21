from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    username = models.CharField(_("username"), max_length=150, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    subscriptions = models.ManyToManyField("currencies.Currency", related_name="subscriptions", blank=True)

    def subscribe(self, currency):
        self.subscriptions.add(currency)

    def unsubscribe(self, currency):
        self.subscriptions.remove(currency)
