from django import forms
from document_catalogue.fields import ClearableFileWidget
from . import models


class DocumentUploadForm(forms.ModelForm):

    class Meta:
        model = models.Document
        fields = ('file', )


class DocumentEditForm(forms.ModelForm):
    file = forms.FileField(widget=ClearableFileWidget())

    class Meta:
        model = models.Document
        fields = ('title', 'description', 'category', 'is_published', 'file')

        widgets = {
            'title'      : forms.TextInput(attrs={'placeholder': 'Document Title (defaults to file name)'}),
            'description': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Optional Description'}),
        }