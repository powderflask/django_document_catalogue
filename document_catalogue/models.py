import os

import django.conf
import mptt.models
from django.apps import apps
from django.db import models
from django.urls import reverse

appConfig = apps.get_app_config("document_catalogue")


class DocumentCategory(mptt.models.MPTTModel):
    """
    A hierarchical category system for assets
    """

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    # sort_order = models.SmallIntegerField(default=1)
    description = models.TextField(blank=True)
    parent = mptt.models.TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    objects = mptt.models.TreeManager()

    class MPTTMeta:
        order_insertion_by = ["slug"]

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["slug"]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse(
            "document_catalogue:category_list",
            kwargs={
                "slug": self.slug,
            },
        )

    def has_children(self):
        """Return true if this DocumentCategory has dependent objects lower in the hierarchy"""
        return self.get_descendant_count() > 0

    def get_document_count(self):
        """Return the total number of documents uploaded for this category"""
        return self.document_set.count()


class DocumentQueryset(models.QuerySet):
    """Custom query set for Document model"""

    def published(self):
        return self.filter(is_published=True)

    def in_category(self, category_slug):
        return self.filter(category__slug=category_slug)


BaseDocumentManager = models.Manager.from_queryset(DocumentQueryset)


class DocumentManager(BaseDocumentManager):
    """Manager for Document model with all methods from DocumentQuerySet."""

    def get_queryset(self):
        return super().get_queryset().select_related("category")


class PublishedDocumentManager(DocumentManager):
    """Published documents only"""

    def get_queryset(self):
        return super().get_queryset().published()


def document_upload_path_callback(instance, filename):
    """Dynamic upload path based on file instance"""
    path = "%s%s/%s" % (appConfig.settings.MEDIA_ROOT, instance.category.slug, filename)
    return path


class Document(models.Model):
    """
    A file and the meta-data describing that file in the catalogue.
    """

    category = models.ForeignKey(DocumentCategory, on_delete=models.CASCADE)

    sort_order = models.PositiveSmallIntegerField(default=0, verbose_name="Order")

    user = models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL, on_delete=models.SET(1)
    )

    creation_date = models.DateTimeField(auto_now_add=True, verbose_name="Created")

    update_date = models.DateTimeField(auto_now=True, verbose_name="Last Modified")

    title = models.CharField(max_length=512)

    description = models.TextField(null=True, blank=True)

    is_published = models.BooleanField(default=False)

    if appConfig.settings.USE_PRIVATE_FILES:
        from private_storage.fields import PrivateFileField

        file = PrivateFileField(
            upload_to=document_upload_path_callback,
            content_types=appConfig.settings.CONTENT_TYPE_WHITELIST,
            max_file_size=appConfig.settings.MAX_FILESIZE
            if appConfig.settings.MAX_FILESIZE
            else None,
        )
    else:
        from constrainedfilefield.fields import ConstrainedFileField

        file = ConstrainedFileField(
            max_length=200,
            upload_to=document_upload_path_callback,
            content_types=appConfig.settings.CONTENT_TYPE_WHITELIST,
            max_upload_size=appConfig.settings.MAX_FILESIZE * 1024 * 1024
            if appConfig.settings.MAX_FILESIZE
            else 0,
        )
    objects = DocumentManager()
    published = PublishedDocumentManager()

    class Meta:
        ordering = ("sort_order",)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "document_catalogue:document_detail",
            kwargs={
                "pk": self.pk,
            },
        )

    def get_edit_url(self):
        return reverse(
            "document_catalogue:document_edit",
            kwargs={
                "pk": self.pk,
            },
        )

    def get_download_url(self):
        return reverse(
            "document_catalogue:document_download",
            kwargs={
                "pk": self.pk,
            },
        )

    def get_filetype(self):
        name, extension = os.path.splitext(self.file.name)
        return extension[1:]

    def filename(self):
        return os.path.basename(self.file.name)

    def save(self, *args, **kwargs):
        if not self.sort_order:
            last = Document.objects.order_by("sort_order").values("sort_order").last()
            self.sort_order = last["sort_order"] + 1 if last else 1
        super().save(*args, **kwargs)
