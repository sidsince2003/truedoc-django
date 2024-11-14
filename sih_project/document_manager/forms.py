from django import forms

class DocumentUploadForm(forms.Form):
    document_type = forms.CharField(max_length=100)
    document = forms.FileField()
    other_type = forms.CharField(max_length=100, required=False)
