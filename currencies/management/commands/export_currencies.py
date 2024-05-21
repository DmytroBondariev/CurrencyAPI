import csv
from django.core.management.base import BaseCommand
from currencies.models import Currency


class Command(BaseCommand):
    help = 'Exports currencies to a local CSV file'

    def handle(self, *args, **options):
        with open('currencies.csv', 'w', newline='') as csvfile:
            fieldnames = ['currency_a', 'currency_b', 'latest_rate_sell', 'latest_rate_buy', 'latest_rate_cross']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for currency in Currency.objects.values(*fieldnames):
                writer.writerow(currency)

        self.stdout.write(self.style.SUCCESS('Successfully exported currencies to currencies.csv'))
