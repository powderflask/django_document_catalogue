from importlib import import_module
from functools import partial
from itertools import groupby

from django.utils.functional import cached_property
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponseForbidden
from django.template.loader import get_template
from django.db.models import Q, Prefetch
from django.db.models.functions import Lower
from django.views import generic

from .models import Document, DocumentCategory
from .views_generic import AjaxOnlyViewMixin
from .decorators import permission_required
from . import settings, forms

permissions = import_module(settings.DOCUMENT_CATALOGUE_PERMISSIONS)


def get_permissions_context(view):
    """ Return a dictionary of permissions (partials that can be called with no arguments) """
    context = {}
    for name in dir(permissions):
        fn = getattr(permissions, name)
        if callable(fn):
            context[name] = partial(fn, view.request.user, **view.kwargs)
    return context


@permission_required(permissions.user_can_view_document_catalogue)
class CatalogueViewMixin(generic.base.ContextMixin, generic.View):
    """ Mixin for all Document Views """
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'show_edit_links': True if settings.DOCUMENT_CATALOGUE_ENABLE_EDIT_URLS else False,
            **get_permissions_context(self),
        })
        return ctx


class CategorySlugViewMixin:
    """ Mixin for views that take a category slug as a URL arg """
    @property
    def category_slug(self):
        return self.kwargs.get('slug', None)

    @cached_property
    def category(self):
        return get_object_or_404(DocumentCategory, slug=self.category_slug)


class DocumentPkMixin:
    """ Mixins for views that take a document pk as a URL arg """
    @property
    def document_pk(self):
        return self.kwargs.get('pk', None)

    @cached_property
    def document(self):
        try:
            return Document.objects.published().select_related('category').get(pk=self.document_pk)
        except Document.DoesNotExist:
            raise Http404


class DocumentListMixin(CatalogueViewMixin, CategorySlugViewMixin):
    """Mixin for views that list documents."""
    @property
    def ordering(self):
        """ Return a Q object representing the ordering to use for document queryset """
        ORDERING_EXPRESSION = {
            'date' : '-update_date',
            'title': Lower('title').asc(),
        }
        ordering = self.request.GET.get('ordering', None)
        return ORDERING_EXPRESSION[ordering] if ordering and ordering in ORDERING_EXPRESSION else None


    def get_queryset(self):
        qs = Document.objects.published().select_related('category', )
        if self.category_slug:
            qs = qs.filter(category__slug=self.category_slug)
        if self.ordering:
            qs = qs.order_by('category', self.ordering)
        return qs

    def get_documents_queryset(self):
        return self.get_queryset()


class DocumentCatalogueListView(DocumentListMixin, generic.ListView):
    """ List all categories in the Catalogue """
    template_name = 'document_catalogue/categories_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'categories': DocumentCategory.objects.add_related_count(
                                DocumentCategory.objects.all(), Document,
                                'category', 'document_counts',cumulative=True
            ),
        })
        return ctx


class CategoryListViewMixin(generic.base.ContextMixin, CategorySlugViewMixin):
    """ Mixin for views that navigate categories or display a list of categories """
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'category': self.category,
            'categories': self.category.get_descendants(include_self=True),
            'breadcrumb': self.category.get_ancestors()
        })
        return ctx


class DocumentCategoryListView(CategoryListViewMixin, DocumentListMixin, generic.ListView):
    """ List all documents in a given category """
    template_name = 'document_catalogue/documents_by_category_list.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        documents = Prefetch('document_set', queryset=self.get_documents_queryset())
        ctx.update({
            'categories': self.category.get_descendants(include_self=True).prefetch_related(documents)
        })
        return ctx

class DocumentViewMixin(generic.base.ContextMixin, DocumentPkMixin):
    """ Mixins for views that display a document """
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'document' : self.document,
            'category' : self.document.category,
            'breadcrumb':self.document.category.get_ancestors()
        })
        return ctx

    def get_document_absolute_uri(self):
        return self.request.build_absolute_uri(self.document.get_download_url())


class DocumentDetailView(CatalogueViewMixin, DocumentViewMixin,  generic.DetailView):
    """ Display detailed information about a single document """
    template_name = 'document_catalogue/document_detail.html'
    model = Document


@permission_required(permissions.user_can_view_document_catalogue)
class DocumentDownloadView(DocumentPkMixin,  generic.RedirectView):
    """ Redirect to the file URL """

    def get_redirect_url(self, *args, **kwargs):
        """ Return the document's file download URL """
        return self.document.file.url


@permission_required(permissions.user_can_edit_document)
class DocumentEditView(CatalogueViewMixin, DocumentViewMixin, generic.UpdateView):
    """ Display detailed information about a single document """
    template_name = 'document_catalogue/document_edit.html'
    model = Document
    form_class = forms.DocumentEditForm


@permission_required(permissions.user_can_delete_document)
class DocumentDeleteView(CatalogueViewMixin, DocumentViewMixin, generic.DeleteView):
    """ Delete a single document """
    model = Document

    @property
    def document(self):
        return self.object

    def get_success_url(self):
        return reverse('document_catalogue:category_list', kwargs={'slug':self.document.category.slug})


class DocumentAjaxAPI(CatalogueViewMixin, CategorySlugViewMixin, DocumentPkMixin, AjaxOnlyViewMixin):
    """
        Async API for document actions
        Plays nice with document_catalogue.js and dropzone
    """
    def save_document(self):
        file = self.request.FILES['file']
        document = Document(
            user=self.request.user,
            title=file.name,
            category=self.category,
            is_published=True,
            file=file
        )
        document.save()
        return document

    def post(self, request, *args, **kwargs):
        if not permissions.user_can_post_document(request.user, **self.kwargs):
            return HttpResponseForbidden('Permission Denied')

        form_class = forms.DocumentUploadForm
        document_template = get_template('document_catalogue/include/documents.html')

        def get_form():
            return form_class(data=request.POST, files=request.FILES)

        # Use the Upload Form to validate the file (mime type and size)
        form = get_form()
        if form.is_valid():
            document = self.save_document()
            html = document_template.render({'document_list': (document, ), **get_permissions_context(self)}),

            return self.render_to_json_response({
                'success': True,
                'document_item': html,
            })
        else:  # Common error handling is completed by dropzone -- this is a hard-fail fallback.
            return HttpResponseForbidden('Invalid request: Form errors %s' % ', '.join(e.as_text() for e in form.errors.values()))

    def delete(self, request, *args, **kwargs):
        if not permissions.user_can_delete_document(request.user, **self.kwargs) :
            return HttpResponseForbidden('Permission Denied')
        if self.document:
            self.document.delete()
            json_context = {"success" : True}
            return self.render_to_json_response(json_context)
        else:
            return HttpResponseForbidden('Invalid request. Document NOT deleted.')

    def get(self, request, *args, **kwargs):
        """ Ajax Search for documents matching search term in ?q= request param """
        search_term = request.GET.get('q', None)

        def format_select2(document):
            return {
                'id'  : document.get_absolute_url(),
                'text': document.title}

        search_options = []
        # Format options as select2 data objects
        if search_term:  # retrieve search results, if a search_term is given
            filter = Q(title__icontains=search_term) | \
                     Q(category__name__icontains=search_term)
            docs = Document.objects.published().filter( filter ).select_related('category')

            search_options = [
                {'text': category.name, 'children': [format_select2(doc) for doc in group] }
                for category, group in groupby(docs, lambda d: d.category)
            ]

        else:  # Recently updated documents.
            recently_updated = Document.objects.published().order_by('-update_date')[:10]
            if recently_updated:
                options = [format_select2(doc) for doc in recently_updated]
                search_options = [{'text': 'Recently Updated', 'children':  options},]

        return self.render_to_json_response({'options': search_options})
