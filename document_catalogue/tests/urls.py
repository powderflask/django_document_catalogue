from django.conf import settings
from django.urls import path, include

urlpatterns = [

    path('documents/', include('document_catalogue.urls')),

    path('private-media/', include('private_storage.urls')),

]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
