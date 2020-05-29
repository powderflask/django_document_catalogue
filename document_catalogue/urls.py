from django.apps import apps
from django.urls import path

from . import views

appConfig = apps.get_app_config('document_catalogue')

app_name = 'document_catalogue'

urlpatterns = [
    path('',
         view=views.DocumentCatalogueListView.as_view(),
         name='catalogue_list'
    ),
    path('category/<slug:slug>/',
         view=views.CategoryDocumentListView.as_view(),
         name='category_list'
         ),
    path('detail/<int:pk>/',
         view=views.DocumentDetailView.as_view(),
         name='document_detail'
    ),
    path('download/<int:pk>/',
         view=views.DocumentDownloadView.as_view(),
         name='document_download'
    ),
    # AJAX API
    path('search/',
         view=views.DocumentAjaxAPI.as_view(),
         name='api_search'
    ),
]

if appConfig.settings.ENABLE_EDIT_URLS:
    urlpatterns += [
        path('edit/<int:pk>/',
             view=views.DocumentEditView.as_view(),
             name='document_edit'
        ),
        path('detail/<int:pk>/delete/',
             view=views.DocumentDeleteView.as_view(),
             name='document_delete'
        ),
        # AJAX API
        path('post/<slug:slug>/',
             view=views.DocumentAjaxAPI.as_view(),
             name='api_post'
        ),
        path('delete/<int:pk>/',
             view=views.DocumentAjaxAPI.as_view(),
             name='api_delete'
        ),
    ]
