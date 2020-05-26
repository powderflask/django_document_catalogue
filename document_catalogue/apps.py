from django.apps import AppConfig


class BaseCatalogueConfig(AppConfig):
    name = 'document_catalogue'
    verbose_name = 'Document Catalogue'


class PrivateCatalogueConfig(BaseCatalogueConfig):
    verbose_name = 'Private Catalogue'

    USE_PRIVATE_FILES = True
    LOGIN_REQUIRED_DEFAULT = True


class PublicCatalogueConfig(BaseCatalogueConfig):
    verbose_name = 'Public Catalogue'

    USE_PRIVATE_FILES = False
    LOGIN_REQUIRED_DEFAULT = False