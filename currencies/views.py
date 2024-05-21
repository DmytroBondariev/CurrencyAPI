from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import generics, status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from currencies.models import Currency, CurrencyHistory
from currencies.serializers import CurrencyInitialSerializer, CurrencyHistorySerializer, CurrencyHistoryDetailSerializer


class CurrencyPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 1000


@extend_schema(
    description="Retrieve a list of all currencies with optional filtering by `currency_a` and `currency_b`.",
    parameters=[
        OpenApiParameter(name="currency_a", description="Filter by currency A", required=False, type=str),
        OpenApiParameter(name="currency_b", description="Filter by currency B", required=False, type=str),
    ],
    responses={200: CurrencyInitialSerializer(many=True)}
)
class CurrencyActualListView(generics.ListAPIView):
    model = Currency
    authentication_classes = (JWTAuthentication,)
    paginator_class = CurrencyPagination

    def get_queryset(self):
        queryset = Currency.objects.all()
        currency_a = self.request.query_params.get("currency_a")
        currency_b = self.request.query_params.get("currency_b")
        query_dict = {"currency_a": currency_a, "currency_b": currency_b}

        if any([currency_a, currency_b]):
            queryset = queryset.filter(**{key: value.upper() for key, value in query_dict.items() if value})

        return queryset

    def get_serializer_class(self):
        return CurrencyInitialSerializer

    def get_permissions(self):
        return [IsAuthenticatedOrReadOnly()]


@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of currencies the user is not subscribed to.",
        responses={200: CurrencyInitialSerializer(many=True)}
    ),
    subscribe=extend_schema(
        description="Subscribe to a currency.",
        responses={200: None, 400: None, 404: None}
    ),
    unsubscribe=extend_schema(
        description="Unsubscribe from a currency.",
        responses={200: None, 400: None, 404: None}
    )
)
class CurrencySubscriptionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    description = "A list of currencies the user is not subscribed to."
    model = Currency
    paginator_class = CurrencyPagination

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user_subscriptions = self.request.user.subscriptions.all()
        queryset = Currency.objects.exclude(id__in=user_subscriptions)
        if self.action == "subscribe" or self.action == "unsubscribe":
            queryset = Currency.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return CurrencyInitialSerializer
        return CurrencyInitialSerializer

    @action(detail=True, methods=['GET'])
    def subscribe(self, request, pk=None):
        try:
            currency = self.get_queryset().get(id=pk)
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Currency not found."})

        if currency not in request.user.subscriptions.all():
            request.user.subscriptions.add(currency)
            return Response(status=status.HTTP_200_OK, data={"detail": "Subscribed."})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Already subscribed."})

    @action(detail=True, methods=['GET'])
    def unsubscribe(self, request, pk=None):
        try:
            currency = self.get_queryset().get(id=pk)
        except Currency.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"detail": "Currency not found."})

        if currency in request.user.subscriptions.all():
            request.user.subscriptions.remove(currency)
            return Response(status=status.HTTP_200_OK, data={"detail": "Unsubscribed."})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Not subscribed."})


@extend_schema(
    description="Retrieve a list of all currency histories with optional filtering by `currency_a` and `currency_b`.",
    parameters=[
        OpenApiParameter(name="currency_a", description="Filter by currency A", required=False, type=str),
        OpenApiParameter(name="currency_b", description="Filter by currency B", required=False, type=str),
    ],
    responses={200: CurrencyHistorySerializer(many=True)}
)
class CurrencyAllHistoriesView(generics.ListAPIView):
    model = CurrencyHistory
    authentication_classes = (JWTAuthentication,)
    paginator_class = CurrencyPagination

    serializer_class = CurrencyHistorySerializer

    def get_queryset(self):
        queryset = CurrencyHistory.objects.select_related("currency").order_by('-datetime')

        currency_a = self.request.query_params.get("currency_a")
        currency_b = self.request.query_params.get("currency_b")
        query_dict = {"currency_a": currency_a, "currency_b": currency_b}

        if currency_a and currency_b:
            currency = Currency.objects.filter(
                **{key: value.upper() for key, value in query_dict.items() if value}).first()
            queryset = CurrencyHistory.objects.filter(currency=currency).order_by("-datetime")

        return queryset

    def get_permissions(self):
        return [IsAuthenticated()]


@extend_schema(
    description="Retrieve the history of a specific currency with optional filtering by `date_from` and `date_to`.",
    parameters=[
        OpenApiParameter(name="date_from", description="Filter by start date", required=False, type=str),
        OpenApiParameter(name="date_to", description="Filter by end date", required=False, type=str),
    ],
    responses={200: CurrencyHistoryDetailSerializer(many=True)}
)
class CurrencyHistoryView(generics.ListAPIView):
    model = CurrencyHistory
    authentication_classes = (JWTAuthentication,)
    serializer_class = CurrencyHistoryDetailSerializer

    def get_queryset(self):
        currency_id = self.kwargs.get('pk')
        queryset = CurrencyHistory.objects.filter(currency_id=currency_id).select_related("currency").order_by(
            '-datetime')

        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if date_from and not date_to:
            queryset = queryset.filter(datetime__gte=date_from)
        elif date_to and not date_from:
            queryset = queryset.filter(datetime__lte=date_to)
        elif date_from and date_to:
            queryset = queryset.filter(datetime__range=[date_from, date_to])

        return queryset

    def get_permissions(self):
        return [IsAuthenticated()]
