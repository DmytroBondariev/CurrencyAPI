from celery import shared_task

from currencies.constants import API_CURRENCIES_MONOBANK
from currencies.management.commands.update_currencies import update_currency
from currencies.serializers import CurrencyInitialSerializer
from currencies.utils import get_currencies_info_all


@shared_task
def update_currencies():
    print()
    print('task is running')
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
