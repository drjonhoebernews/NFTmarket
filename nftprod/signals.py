from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, post_migrate
from django.dispatch import receiver
from django.utils import timezone
from nftprod.models import Like, Bid, History, NFT, SaleType, Currency, MediaType, Category, Ownership
from django.db.models import Subquery, Max, OuterRef


@receiver(post_migrate)
def create_default_sale_types(sender, **kwargs):
    if sender.name == 'nftprod':  # yourappname'i kendi uygulama adınızla değiştirin
        default_sale_types = SaleType.get_default_sale_types()
        for sale_type in default_sale_types:
            SaleType.objects.get_or_create(name=sale_type['name'], description=sale_type['description'])


@receiver(post_migrate)
def create_default_currency(sender, **kwargs):
    if sender.name == 'nftprod':  # yourappname'i kendi uygulama adınızla değiştirin
        default_currencys = Currency.get_default_currency()
        for currency in default_currencys:
            Currency.objects.get_or_create(name=currency['name'], symbol=currency['symbol'], decimals=currency['decimals'], contract=currency['contract'])


@receiver(post_migrate)
def create_default_mediatype(sender, **kwargs):
    if sender.name == 'nftprod':  # yourappname'i kendi uygulama adınızla değiştirin
        default_mediatypes = MediaType.get_default_mediatype()
        for mediatype in default_mediatypes:
            MediaType.objects.get_or_create(name=mediatype['name'], extension=mediatype['extension'])


@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'nftprod':
        default_categories = {
            'Sanat': 'Sanat kategorisi altında, farklı sanat türlerindeki NFT\'ler yer alır.',
            'Spor': 'Spor kategorisi altında, farklı sporlarla ilgili NFT\'ler yer alır.',
            'Oyun': 'Oyun kategorisi altında, farklı oyun türlerindeki NFT\'ler yer alır.',
            'Müzik': 'Müzik kategorisi altında, farklı müzik türlerindeki NFT\'ler yer alır.',
            'Metaverse': 'Metaverse kategorisi altında, NFT\'lerin sanal dünyalarla ilgili özellikleri yer alır.',
            'Koleksiyon': 'Koleksiyon kategorisi altında, farklı NFT koleksiyonları yer alır.'
        }
        for category_name, category_description in default_categories.items():
            Category.objects.get_or_create(name=category_name, description=category_description)


@receiver(post_migrate)
def create_user(sender, **kwargs):
    if sender.name == 'nftprod':
        default_users = {
            'deneme1': '2238dr',
            'deneme2': '2238dr',
            'deneme3': '2238dr',
            'deneme4': '2238dr',
        }
        for user_username, user_password in default_users.items():
            User.objects.get_or_create(username=user_username, password=user_password)


@receiver(post_save, sender=Like)
def update_nft_like_count_on_like_save(sender, instance, created, **kwargs):
    if created:
        instance.nft.like_count += 1
    instance.nft.save()


@receiver(post_delete, sender=Like)
def update_nft_like_count_on_like_delete(sender, instance, **kwargs):
    instance.nft.like_count -= 1
    instance.nft.save()


@receiver(post_save, sender=Bid)
def update_nft_bid_count_on_bid_save(sender, instance, created, **kwargs):
    if created:
        instance.nft.bit_count += 1
    instance.nft.save()


@receiver(post_save, sender=NFT)
def nft_saved(sender, instance, created, **kwargs):
    # NFT OLUŞTUR
    if created:
        Ownership.objects.create(
            user=instance.creater,
            nft=instance,
            price_amount=instance.price_amount,
            price_currency=instance.price_currency,
            owned_at=timezone.now()
        )


@receiver(post_save, sender=NFT)
def nft_saved(sender, instance, created, **kwargs):
    # NFT OLUŞTUR
    if created:
        History.objects.create(
            nft=instance,
            user=instance.creater,
            type='create',
            price_amount=instance.price_amount,
            price_currency=instance.price_currency,
            date=timezone.now()
        )


@receiver(post_save, sender=Bid)
def update_nft_highest_bid(sender, instance, created, **kwargs):
    if created:
        # Get the highest bid for this NFT
        highest_bid = Bid.objects.filter(nft=instance.nft)\
                                 .order_by('-price_amount')\
                                 .values('price_amount')[:1]
        # Update the NFT's highest_bid field with the highest bid price
        NFT.objects.filter(pk=instance.nft.pk)\
                   .update(highest_bid=Subquery(highest_bid))


@receiver(post_save, sender=Bid)
def bid_saved(sender, instance, created, **kwargs):
    # Teklif kaydı yap
    if created:
        History.objects.create(
            nft=instance.nft,
            user=instance.user,
            type='bid',
            price_amount=instance.price_amount,
            price_currency=instance.price_currency,
            date=timezone.now()
        )


@receiver(post_delete, sender=Bid)
def bid_deleted(sender, instance, **kwargs):
    # Teklif silindiği zaman kaydı yap
    History.objects.create(
        nft=instance.nft,
        user=instance.user,
        type='delete',
        price_amount=instance.price_amount,
        price_currency=instance.price_currency,
        date=timezone.now()
    )
