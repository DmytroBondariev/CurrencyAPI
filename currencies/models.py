from django.db import models


class Currency(models.Model):
    currency_a = models.CharField(max_length=3)
    currency_b = models.CharField(max_length=3)
    latest_rate_sell = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    latest_rate_buy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    latest_rate_cross = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    class Meta:
        ordering = ["currency_a"]
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        unique_together = ["currency_a", "currency_b"]

    def __str__(self):
        return f"{self.currency_a}/{self.currency_b}"


class CurrencyHistory(models.Model):
    datetime = models.DateTimeField()
    rate_buy = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rate_sell = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    rate_cross = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    currency = models.ForeignKey("Currency", on_delete=models.CASCADE, related_name="currency")

    class Meta:
        ordering = ["datetime"]
        verbose_name = "Currency_History"
        verbose_name_plural = "Currencies_Histories"
        unique_together = ["currency", "datetime"]

    def __str__(self):
        return f"rate_cross: {self.rate_cross}" if self.rate_cross \
            else f"rate_buy: {self.rate_buy}, rate_sell: {self.rate_sell}"
