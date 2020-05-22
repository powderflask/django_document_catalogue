import os
import django.conf
from . import settings
from django.urls import reverse
from django.db import models
import mptt.models


class DocumentCategory(mptt.models.MPTTModel):
    """
        A hierarchical category system for assets
    """
    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    # sort_order = models.SmallIntegerField(default=1)
    description = models.TextField(blank=True)
    parent = mptt.models.TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    objects = mptt.models.TreeManager()  # this is the default manager, but pydev was being irritating - just to shut-up pydev - can be removed without any other effect

    class MPTTMeta:
        order_insertion_by = ['slug']

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['slug']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('document_catalogue:category_list', kwargs={'slug': self.slug, })

    def has_children(self):
        """ Return true if this DocumentCategory has dependent objects lower in the hierarchy """
        return self.get_descendant_count() > 0

    def document_count(self):
        """ Return the total number of documents uploaded for this category """
        return self.document_set.count()


class DocumentManager(models.Manager):
    """Custom query manager for the Document model."""
    def published(self):
        """ Returns queryset of published documents """
        return self.get_queryset().filter(is_published=True)

    def in_category(self, category_slug):
        return self.get_queryset().filter(category__slug=category_slug)


def document_upload_path_callback(instance, filename):
    """ Dynamic upload path based on file instance """
    path = "%s%s/%s" % (settings.DOCUMENT_CATALOGUE_MEDIA_ROOT, instance.category.slug, filename)
    return path


class Document(models.Model):
    """
    A document consists of a title and description and a number of filer-files.
    """
    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)

    sort_order = models.PositiveSmallIntegerField(default=1)

    user = models.ForeignKey(django.conf.settings.AUTH_USER_MODEL, on_delete=models.SET(1))

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Created')

    update_date = models.DateTimeField(auto_now=True, verbose_name='Last Modified')

    title = models.CharField(max_length=512)

    description = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False)

    if settings.DOCUMENT_CATALOGUE_USE_PRIVATE_FILES:
        from private_storage.fields import PrivateFileField
        file = PrivateFileField(
            upload_to=document_upload_path_callback,
            content_types=settings.DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST,
            max_file_size=settings.DOCUMENT_CATALOGUE_MAX_FILESIZE \
                                                            if settings.DOCUMENT_CATALOGUE_MAX_FILESIZE else None
        )
    else:
        from constrainedfilefield.fields import ConstrainedFileField
        file = ConstrainedFileField(max_length=200,
            upload_to=document_upload_path_callback,
            content_types=settings.DOCUMENT_CATALOGUE_CONTENT_TYPE_WHITELIST,
            max_upload_size=settings.DOCUMENT_CATALOGUE_MAX_FILESIZE * 1024 * 1024 \
                                                            if settings.DOCUMENT_CATALOGUE_MAX_FILESIZE else 0
        )
    objects = DocumentManager()

    class Meta:
        ordering = ('category', 'sort_order', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('document_catalogue:document_detail', kwargs={'pk': self.pk, })

    def get_edit_url(self):
        return reverse('document_catalogue:document_edit', kwargs={'pk': self.pk, })

    def get_download_url(self):
        return reverse('document_catalogue:document_download', kwargs={'pk': self.pk, })

    def get_filetype(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:]
