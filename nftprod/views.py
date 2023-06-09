import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import HttpResponse
from .models import NFT, Category, Collection, Property, Tag, MediaType, NFTMedia, Currency
from .serializers import NFTRetrieveSerializer, NFTCreateSerializer, CategorySerializer, CategoryCreateSerializer, \
    CollectionSerializer, CollectionCreateSerializer, PropertySerializer, PropertyCreateSerializer, TagSerializer, \
    TagCreateSerializer, MediaTypeSerializer, NFTMediaSerializer, NFTMediaCreateSerializer, PriceCurrencySerializer, \
    PriceCurrencyCreateSerializer


class NFTListCreateView(generics.ListCreateAPIView):
    queryset = NFT.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NFTRetrieveSerializer
        elif self.request.method == 'POST':
            return NFTCreateSerializer


class NFTRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NFT.objects.all()
    serializer_class = NFTRetrieveSerializer
    lookup_field = 'token_id'


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategorySerializer
        elif self.request.method == 'POST':
            return CategoryCreateSerializer


class CollectionListCreateView(generics.ListCreateAPIView):
    queryset = Collection.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CollectionSerializer
        elif self.request.method == 'POST':
            return CollectionCreateSerializer


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PropertySerializer
        elif self.request.method == 'POST':
            return PropertyCreateSerializer


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TagSerializer
        elif self.request.method == 'POST':
            return TagCreateSerializer


class MediaTypeListView(generics.ListAPIView):
    queryset = MediaType.objects.all()
    serializer_class = MediaTypeSerializer


class NFTMediaListCreateView(generics.ListCreateAPIView):
    queryset = NFTMedia.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NFTMediaSerializer
        elif self.request.method == 'POST':
            return NFTMediaCreateSerializer


class PriceCurrencyListCreateView(generics.ListCreateAPIView):
    queryset = Currency.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PriceCurrencySerializer
        elif self.request.method == 'POST':
            return PriceCurrencyCreateSerializer


def update_currencies(request):
    currencies = Currency.objects.filter(is_active=True)
    for currency in currencies:
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={currency.name.lower()}&vs_currencies=usd,eur,try')
            prices = response.json()[currency.name.lower()]
            currency.usd_value = prices['usd']
            currency.eur_value = prices['eur']
            currency.try_value = prices['try']
            currency.save()
        except Exception as e:
            print(f'Error updating {currency.name}: {e}')
    return HttpResponse('Currencies updated')
