from django.urls import path, include
from rest_framework.routers import SimpleRouter

from currencies.views import CurrencyActualListView, CurrencyAllHistoriesView, CurrencyHistoryView, \
    CurrencySubscriptionViewSet

currencies_list = CurrencyActualListView.as_view()
currencies_history_list = CurrencyAllHistoriesView.as_view()
currency_history_detail = CurrencyHistoryView.as_view()
router = SimpleRouter()
router.register(r"subscriptions", CurrencySubscriptionViewSet, basename="subscriptions")

urlpatterns = [
    path("all/", currencies_list, name="currency-all-list"),
    path("history/", currencies_history_list, name="currency-all-history-list"),
    path("history/<int:pk>", currency_history_detail, name="currency-history-detail"),
    path("", include(router.urls)),

]

app_name = "currencies"
