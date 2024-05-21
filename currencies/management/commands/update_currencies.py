from django.core.management.base import BaseCommand

from currencies.constants import API_CURRENCIES_MONOBANK, CURRENCIES_ISO_DICT
from currencies.models import Currency
from currencies.serializers import CurrencyHistorySerializer
from currencies.utils import get_currencies_info_all


class Command(BaseCommand):
    help = 'Updates currencies history list'

    def handle(self, *args, **options):
        update_currency(get_currencies_info_all(API_CURRENCIES_MONOBANK))


def update_currency_rate(currency, data):
    currency.latest_rate_buy = data.get('rateBuy', None)
    currency.latest_rate_sell = data.get('rateSell', None)
    currency.latest_rate_cross = data.get('rateCross', None)
    currency.save()


def update_currency(api_response):
    for currency in api_response:
        currency_a = CURRENCIES_ISO_DICT[currency.pop('currencyCodeA')]
        currency_b = CURRENCIES_ISO_DICT[currency.pop('currencyCodeB')]
        currency_object = Currency.objects.get(currency_a=currency_a, currency_b=currency_b)

        if any(
                [
                    currency_object.latest_rate_buy != currency.get('rateBuy', None),
                    currency_object.latest_rate_sell != currency.get('rateSell', None),
                    currency_object.latest_rate_cross != currency.get('rateCross', None)
                ]
        ):
            update_currency_rate(currency_object, currency)

        currency["currency"] = currency_object.id

        serializer = CurrencyHistorySerializer(data=currency)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
