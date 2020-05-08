from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name='home'),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('documents/', include('document_catalogue.urls')),

    path('private-media/', include('private_storage.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
