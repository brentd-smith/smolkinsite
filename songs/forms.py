# -*- coding: utf-8 -*-

from django import forms
from .models import Document

# class DocumentForm(forms.Form):
#     docfile = forms.FileField(
#         label='Select a file'
#     )

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
