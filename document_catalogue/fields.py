"""
ConstrainedFileField Taken directly from django-constrainedfilefield  https://github.com/mbourqui/django-constrainedfilefield
"""
import os

from django import forms
from django.conf import settings
from django.db import models
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


class ConstrainedFileField(models.FileField):
    """
    A FileField with additional constraints. Namely, the file size and type can be restricted. If
    using the types, the magic library is required. Setting neither a file size nor type behaves
    like a regular FileField.
    Parameters
    ----------
    content_types : list of str
        List containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
    max_upload_size : int
        Maximum file size allowed for upload, in bytes
            1 MB - 1048576 B - 1024**2 B - 2**20 B
            2.5 MB - 2621440 B
            5 MB - 5242880 B
            10 MB - 10485760 B
            20 MB - 20971520 B
            33 MiB - 2**25 B
            50 MB - 5242880 B
            100 MB 104857600 B
            250 MB - 214958080 B
            500 MB - 429916160 B
            1 GiB - 1024 MiB - 2**30 B
    js_checker : bool
        Add a javascript file size checker to the form field
    mime_lookup_length : int
    See Also
    --------
    Based on https://github.com/kaleidos/django-validated-file/blob/master/validatedfile/fields.py
    With inspiration from http://stackoverflow.com/a/9016664
    """

    description = _("A file field with constraints on size and/or type")

    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop("max_upload_size", 0)
        assert isinstance(self.max_upload_size, int) and self.max_upload_size >= 0
        self.content_types = kwargs.pop("content_types", [])
        self.mime_lookup_length = kwargs.pop("mime_lookup_length", 4096)
        assert isinstance(self.mime_lookup_length, int) and self.mime_lookup_length >= 0
        self.js_checker = kwargs.pop("js_checker", False)

        super(ConstrainedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ConstrainedFileField, self).clean(*args, **kwargs)

        if self.max_upload_size and data.size > self.max_upload_size:
            # Ensure no one bypasses the js checker
            raise forms.ValidationError(
                _('File size exceeds limit: %(current_size)s. Limit is %(max_size)s.') %
                {'max_size': filesizeformat(self.max_upload_size),
                 'current_size': filesizeformat(data.size)})

        if self.content_types:
            import magic
            file = data.file
            uploaded_content_type = getattr(file, 'content_type', '')

            # magic_file_path used only for Windows.
            magic_file_path = getattr(settings, "MAGIC_FILE_PATH", None)
            if magic_file_path and os.name == 'nt':
                mg = magic.Magic(mime=True, magic_file=magic_file_path)
            else:
                mg = magic.Magic(mime=True)
            content_type_magic = mg.from_buffer(file.read(self.mime_lookup_length))
            file.seek(0)

            # Prefer mime-type from magic over mime-type from http header
            if uploaded_content_type != content_type_magic:
                uploaded_content_type = content_type_magic

            if uploaded_content_type not in self.content_types:
                raise forms.ValidationError(
                    _('Unsupported file type: %(type)s. Allowed types are %(allowed)s.') %
                    {'type': content_type_magic,
                     'allowed': self.content_types})
        return data

    def formfield(self, **kwargs):
        """
        Usual Form for a django.models.FileField with optional javascript file size
        checker. Can thus be customized as any other Form for a django.models.FileField.
        Parameters
        ----------
        kwargs
            will be passed to super().formfield()
        Returns
        -------
        django.forms.FileField
        """
        formfield = super(ConstrainedFileField, self).formfield(**kwargs)
        if self.js_checker:
            formfield.widget.attrs.update(
                {'onchange': 'validateFileSize(this, 0, %d);' % (self.max_upload_size,)})
        return formfield

    def deconstruct(self):
        name, path, args, kwargs = super(ConstrainedFileField, self).deconstruct()
        if self.max_upload_size:
            kwargs["max_upload_size"] = self.max_upload_size
        if self.content_types:
            kwargs["content_types"] = self.content_types
        if self.mime_lookup_length:
            kwargs["mime_lookup_length"] = self.mime_lookup_length
        if self.js_checker:
            kwargs["js_checker"] = self.js_checker
        return name, path, args, kwargs

    def __str__(self):
        if hasattr(self, 'model'):
            return super(ConstrainedFileField).__str__()
        else:
            return self.__class__.__name__

class ConstrainedFileWidget(forms.widgets.ClearableFileInput):
    template_name = 'document_catalogue/include/inline_clearable_file_input.html'

