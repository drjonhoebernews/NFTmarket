from django.apps import AppConfig


class NftprodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nftprod'

    def ready(self):
        import nftprod.signals