from django.conf import settings
from django.apps import apps
from django.urls import path, include
from django.conf.urls.static import static

appConfig = apps.get_app_config('document_catalogue')

urlpatterns = [

    path('documents/', include('document_catalogue.urls')),

]

if appConfig.USE_PRIVATE_FILES:
    urlpatterns += [
        path('private-media/', include('private_storage.urls')),

    ]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
