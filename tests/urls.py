from django.apps import apps
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

appConfig = apps.get_app_config("document_catalogue")

urlpatterns = [
    path("documents/", include("document_catalogue.urls")),
]

if appConfig.USE_PRIVATE_FILES:
    urlpatterns += [
        path("private-media/", include("private_storage.urls")),
    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
