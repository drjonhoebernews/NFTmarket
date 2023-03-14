from rest_framework import serializers
from .models import NFT, Category, User, Ownership, Collection, Bid, NFTMedia, Property, Tag, Like, Currency, History, \
    SaleType, MediaType


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PriceCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PriceCurrencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class OwnershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    price_currency = PriceCurrencySerializer()

    class Meta:
        model = Ownership
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Collection
        fields = '__all__'


class CollectionCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Collection
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    price_currency = PriceCurrencySerializer()

    class Meta:
        model = Bid
        fields = '__all__'


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = '__all__'


class NFTMediaSerializer(serializers.ModelSerializer):
    media_type = MediaTypeSerializer()

    class Meta:
        model = NFTMedia
        fields = '__all__'


class NFTMediaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTMedia
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    price_currency = PriceCurrencySerializer()

    class Meta:
        model = History
        fields = '__all__'


class SaleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleType
        fields = '__all__'


class NFTRetrieveSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    creater = UserSerializer()
    collection = CollectionSerializer()
    properties = PropertySerializer(many=True)
    tags = TagSerializer(many=True)
    history = serializers.SerializerMethodField()
    price_currency = PriceCurrencySerializer()
    like = serializers.SerializerMethodField()
    bid = serializers.SerializerMethodField()
    media = NFTMediaSerializer()
    ownerships = serializers.SerializerMethodField()
    sale_type = SaleTypeSerializer()

    @staticmethod
    def get_ownerships(obj):
        ownerships = obj.ownerships.all()
        return OwnershipSerializer(ownerships, many=True).data

    @staticmethod
    def get_history(obj):
        historys = obj.history.all()
        return HistorySerializer(historys, many=True).data

    @staticmethod
    def get_like(obj):
        likes = obj.like.all()
        return LikeSerializer(likes, many=True).data

    @staticmethod
    def get_bid(obj):
        bids = obj.bid.all()
        return BidSerializer(bids, many=True).data

    class Meta:
        model = NFT
        fields = '__all__'


class NFTCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFT
        fields = '__all__'
        read_only_fields = ('token_id', 'slug', 'published_at', 'latest_bid', 'like_count', 'highest_bid')
