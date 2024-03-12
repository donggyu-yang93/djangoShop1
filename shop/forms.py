from .models import Comment, Product
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content',]

