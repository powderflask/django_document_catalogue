from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import DocumentCategory, Document


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    prepopulated_fields = {"slug" : ("name",)}
admin.site.register(DocumentCategory, CategoryAdmin)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'creation_date', 'update_date')
    list_editable = ('category', 'is_published')
admin.site.register(Document, DocumentAdmin)
