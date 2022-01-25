from django.apps import AppConfig

from commerce.settings import DEFAULT_AUTO_FIELD


class AuctionsConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'auctions'
