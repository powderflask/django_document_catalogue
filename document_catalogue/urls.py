from django.urls import path

from . import settings
from . import views


urlpatterns = [
    path('',
         view = views.DocumentCatalogueListView.as_view(),
         name = 'document_catalogue_list'
    ),
    path('category/<slug:slug>/',
         view = views.DocumentCategoryListView.as_view(),
         name = 'document_catalogue_category_list'
    ),
    path('detail/<int:pk>/',
         view = views.DocumentDetailView.as_view(),
         name = 'document_catalogue_detail'
    ),
    path('detail/<int:pk>/delete/',
         view=views.DocumentDetailView.as_view(),
         name='document_catalogue_delete'
         ),
]

if settings.DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS:
    urlpatterns += [
        path('edit/<int:pk>/',
             view = views.DocumentEditView.as_view(),
             name = 'document_catalogue_edit'
        ),
        path('post/<slug:slug>/',
             view = views.DocumentAjaxAPI.as_view(),
             name = "document_catalogue_ajax_post"
        ),
        path('delete/<int:pk>/',
             view = views.DocumentAjaxAPI.as_view(),
             name = "document_catalogue_ajax_delete"
        ),
    ]
