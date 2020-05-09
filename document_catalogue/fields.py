from django import forms


class ClearableFileWidget(forms.widgets.ClearableFileInput):
    template_name = 'document_catalogue/include/inline_clearable_file_input.html'

