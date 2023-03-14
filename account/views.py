from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Kullanıcının kimlik bilgilerini doğrula
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Kullanıcı başarıyla doğrulandı, oturum aç
        login(request, user)
        return Response({'message': 'Oturum açıldı'})
    else:
        # Kullanıcı doğrulanamadı, hata mesajı döndür
        return Response({'message': 'Kullanıcı adı veya şifre yanlış'}, status=status.HTTP_401_UNAUTHORIZED)
