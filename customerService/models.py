from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CsList(models.Model):
    title = models.CharField(max_length=30, null=True, default='None')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='CS_author_question')


class Comment(models.Model):
    cs_list = models.ForeignKey(CsList, on_delete=models.CASCADE, related_name='CS_comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='CS_author_comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)



