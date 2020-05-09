from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import DocumentCategory, Document


@admin.register(DocumentCategory)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register((Document))
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_published', 'creation_date', 'update_date')
    list_editable = ('category', 'is_published')
