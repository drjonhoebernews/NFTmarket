from django.urls import path
from .views import NFTListCreateView, NFTRetrieveUpdateDeleteView, CategoryListCreateView, CollectionListCreateView, \
    PropertyListCreateView, TagListCreateView, MediaTypeListView, NFTMediaListCreateView, PriceCurrencyListCreateView, \
    update_currencies

app_name = 'nftprod'
urlpatterns = [
    path('list', NFTListCreateView.as_view(), name='nftlist'),
    path('<str:token_id>', NFTRetrieveUpdateDeleteView.as_view(), name='nftdetail'),
    path('category/list', CategoryListCreateView.as_view(), name='categorylist'),
    path('collection/list', CollectionListCreateView.as_view(), name='collectionlist'),
    path('property/list', PropertyListCreateView.as_view(), name='propertylist'),
    path('tag/list', TagListCreateView.as_view(), name='taglist'),
    path('mediatype/list', MediaTypeListView.as_view(), name='mediatypelist'),
    path('nftmedia/list', NFTMediaListCreateView.as_view(), name='nftmedialist'),
    path('currency/list', PriceCurrencyListCreateView.as_view(), name='pricecurrencylist'),



    # cron job tanımlanacak yad redis kurulacak
    path('update_currencies/update', update_currencies, name='update'),
]