
# coding: utf-8
from __future__ import unicode_literals

__author__ = 'jujbob'

from django import forms
from .models import Post, SubComment, Resource
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

class SubCommentForm(forms.ModelForm):
    class Meta:
        model = SubComment
        fields = ('text',)

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ('image_file', 'external_url', )
   #     exclude = ('filtered_image_file', )
