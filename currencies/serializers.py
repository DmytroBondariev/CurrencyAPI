from datetime import datetime, timezone
from rest_framework import serializers

from currencies.models import Currency, CurrencyHistory
from currencies.constants import CURRENCIES_ISO_DICT


class CurrencyInitialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("currency_a", "currency_b", "latest_rate_sell", "latest_rate_buy", "latest_rate_cross")
        read_only_fields = ("latest_rate_sell", "latest_rate_buy", "latest_rate_cross")

    def to_internal_value(self, data):
        # date = data.pop('date')
        # data['datetime'] = datetime.fromtimestamp(date, timezone.utc)
        data['currency_a'] = CURRENCIES_ISO_DICT[data.pop('currencyCodeA')]
        data['currency_b'] = CURRENCIES_ISO_DICT[data.pop('currencyCodeB')]
        data['latest_rate_buy'] = data.pop('rateBuy', None)
        data['latest_rate_sell'] = data.pop('rateSell', None)
        data['latest_rate_cross'] = data.pop('rateCross', None)

        return super().to_internal_value(data.copy())

    def validate(self, data):
        if data['currency_a'] == data['currency_b']:
            raise serializers.ValidationError("Currency A and Currency B must be different currencies.")

        return super().validate(data)


class CurrencyHistorySerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField()
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all())

    class Meta:
        model = CurrencyHistory
        fields = ("datetime", "rate_buy", "rate_sell", "rate_cross", "currency", "id")

    def to_internal_value(self, data):
        date = data.pop('date')
        data['datetime'] = datetime.fromtimestamp(date, timezone.utc)
        data['rate_buy'] = data.pop('rateBuy', None)
        data['rate_sell'] = data.pop('rateSell', None)
        data['rate_cross'] = data.pop('rateCross', None)

        return super().to_internal_value(data.copy())

    def validate(self, data):
        if data['datetime'] > datetime.now(timezone.utc):
            raise serializers.ValidationError("Datetime if currency value cannot be in the future.")

        return super().validate(data)


class CurrencyHistoryDetailSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()

    class Meta:
        model = CurrencyHistory
        fields = ("id", "datetime", "rate_buy", "rate_sell", "rate_cross", "currency")
        read_only_fields = ("datetime", "rate_buy", "rate_sell", "rate_cross", "currency")

    @staticmethod
    def get_currency(obj):
        return f"{obj.currency.currency_a}/{obj.currency.currency_b}"
