from django.core.management.base import BaseCommand

from currencies.constants import API_CURRENCIES_MONOBANK
from currencies.management.commands.update_currencies import update_currency
from currencies.serializers import CurrencyInitialSerializer
from currencies.utils import get_currencies_info_all


class Command(BaseCommand):
    help = 'Creates initial currencies list'

    def handle(self, *args, **options):
        response = get_currencies_info_all(API_CURRENCIES_MONOBANK)

        for currency in response:
            serializer = CurrencyInitialSerializer(
                data={
                    "currencyCodeA": currency["currencyCodeA"],
                    "currencyCodeB": currency["currencyCodeB"]
                }
            )
            if serializer.is_valid(raise_exception=False):
                serializer.save()

        update_currency(response)

