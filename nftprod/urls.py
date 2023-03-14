from django.urls import path
from .views import NFTListCreateView, NFTRetrieveUpdateDeleteView

app_name = 'nftprod'
urlpatterns = [
    path('list', NFTListCreateView.as_view(), name='nftlist'),
    path('<str:token_id>', NFTRetrieveUpdateDeleteView.as_view(), name='nftdetail'),
]