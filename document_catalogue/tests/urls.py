from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('documents/', include('document_catalogue.urls')),

    path('private-media/', include('private_storage.urls')),

]

if settings.STANDALONE_MODE:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
