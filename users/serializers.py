from django.contrib.auth import get_user_model
from rest_framework import serializers
from currencies.models import Currency


class UserSerializer(serializers.ModelSerializer):
    subscriptions = serializers.PrimaryKeyRelatedField(many=True, queryset=Currency.objects.all())

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "first_name", "last_name", "subscriptions")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5,
                "style": {"input_type": "password"}
            }
        }

    def create(self, validated_data):
        subscriptions = validated_data.pop('subscriptions', [])
        user = get_user_model().objects.create_user(**validated_data)
        for currency in subscriptions:
            user.subscriptions.add(currency)

        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['subscriptions'] = [
            f"{currency.currency_a}/{currency.currency_b}"
            for currency in instance.subscriptions.all()
        ]

        return representation
