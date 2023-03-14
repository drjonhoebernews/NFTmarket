from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import NFT
from .serializers import NFTRetrieveSerializer, NFTCreateSerializer


class NFTListCreateView(generics.ListCreateAPIView):
    queryset = NFT.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return NFTRetrieveSerializer
        elif self.request.method == 'POST':
            return NFTCreateSerializer


class NFTRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NFT.objects.all()
    serializer_class = NFTRetrieveSerializer
    lookup_field = 'token_id'
