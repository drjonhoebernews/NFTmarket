import json
import uuid
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


def get_collection_media_path(instance, filename):
    return f"nft_{instance.slug}/{filename}"


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    cover = models.FileField(upload_to=get_collection_media_path)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Property(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, editable=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MediaType(models.Model):
    name = models.CharField(max_length=50)
    extension = models.CharField(max_length=50)

    def __str__(self):
        return self.name + ' ' + self.extension

    @staticmethod
    def get_default_mediatype():
        return [
            {'name': 'VIDEO', 'extension': 'mpg4'},
            {'name': 'GIF', 'extension': 'gif'},
            {'name': 'IMAGE', 'extension': 'png'},
            {'name': 'MUSIC', 'extension': 'mp3'},
        ]


def get_media_path(instance, filename):
    return f"nft/{filename}"


class NFTMedia(models.Model):
    media_type = models.ForeignKey(MediaType, on_delete=models.CASCADE)
    media_file = models.FileField(upload_to=get_media_path)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.id and not self.url:
            self.url = self.media_file.url
        super(NFTMedia, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.media_file.delete()
        super(NFTMedia, self).delete(*args, **kwargs)


class Currency(models.Model):
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    decimals = models.IntegerField(default=18)
    contract = models.CharField(max_length=42, unique=True)
    usd_value = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    eur_value = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    try_value = models.DecimalField(max_digits=8, decimal_places=2, default=1)


    def __str__(self):
        return self.name

    @staticmethod
    def get_default_currency():
        return [
            {'name': 'wETH', 'symbol': 'wETH', 'decimals': '18', 'contract': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'},
            {'name': 'PRIOR', 'symbol': 'PRT', 'decimals': '18', 'contract': 'TAwdgYhg3ar64yzPCNpgo5WrQ8rT3R2gsp'},
        ]


class SaleType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_default_sale_types():
        return [
            {
                'name': 'Fixed Price',
                'description': 'Fixed price sale: NFTs are sold at a predetermined price set by the seller.'
            },
            {
                'name': 'Auction',
                'description': 'Auction sale: NFTs are sold to the highest bidder at the end of the bidding period.'
            },
            {
                'name': 'Dutch Auction',
                'description': 'Dutch auction sale: The seller starts with a high price, which is then lowered until a buyer is found.'
            },
            {
                'name': 'Reserve Auction',
                'description': 'Reserve auction sale: A minimum price is set by the seller, and the NFT is sold to the highest bidder who meets that minimum price.'
            },
            {
                'name': 'Renting',
                'description': 'Renting sale: NFTs are rented out for a period of time in exchange for a fee.'
            }
        ]


class NFT(models.Model):
    title = models.CharField(max_length=100)
    token_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, null=False, blank=False)
    slug = models.SlugField(unique=True, null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)
    price_amount = models.DecimalField(max_digits=18, decimal_places=16)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    latest_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    like_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category)
    description = models.TextField(blank=True)

    metadata = models.JSONField(blank=True)

    auction_date = models.DateTimeField(null=True, blank=True)

    bit_count = models.PositiveIntegerField(default=0)

    creater = models.ForeignKey(User, on_delete=models.CASCADE, related_name='nft_creater', blank=True, null=True)

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    media = models.ForeignKey(NFTMedia, on_delete=models.CASCADE, related_name='media_nft')

    properties = models.ManyToManyField(Property, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    highest_bid = models.DecimalField(max_digits=18, decimal_places=16, null=True, blank=True)
    sale_type = models.ForeignKey(SaleType, on_delete=models.SET_NULL, null=True, blank=True, related_name='saletype_nft')
    level = models.CharField(max_length=20, default='beginner')
    language = models.CharField(max_length=50, default='english')
    rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.token_id:
            self.token_id = uuid.uuid4()
        if not self.metadata:
            metadata = {
                'name': self.title,
                'description': self.description,
                'image': self.media.url.__str__(),
                'external_url': self.token_id.__str__()
            }
            self.metadata = json.dumps(metadata)
        super(NFT, self).save(*args, **kwargs)


class Like(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.SET_NULL, null=True, related_name='like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    like_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nft.title + ' / ' + self.user.username


class Bid(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.SET_NULL, null=True, related_name='bid')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids_ownership')
    price_amount = models.DecimalField(max_digits=18, decimal_places=16)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    bid_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.nft.title + ' ' + str(self.price_amount) + ' ' + str(self.bid_date)


class History(models.Model):
    nft = models.ForeignKey(NFT, on_delete=models.SET_NULL, null=True, related_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    type = models.CharField(max_length=100, null=False, blank=False)
    price_amount = models.DecimalField(max_digits=18, decimal_places=16)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + self.type + ' ' + str(self.date)


class Ownership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors')
    nft = models.ForeignKey(NFT, on_delete=models.CASCADE, related_name='ownerships', null=True, default=None)
    price_amount = models.DecimalField(max_digits=18, decimal_places=16)
    price_currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    owned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' ' + str(self.price_amount) + ' ' + str(self.price_currency)