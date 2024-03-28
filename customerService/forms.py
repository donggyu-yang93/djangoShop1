from .models import CsList
from django import forms


class UploadForm(forms.ModelForm):
    class Meta:
        model = CsList
        fields = ['title','content']

