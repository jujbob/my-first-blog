
# coding: utf-8
from __future__ import unicode_literals

from blog import models

__author__ = 'jujbob'

from django import forms
from .models import Post, SubComment, Resource
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class PostResourceForm(forms.ModelForm):
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

    images = forms.CharField()
    class Meta:
        model = Resource
        fields = ('image_file', 'external_url', 'images')

    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields["images"].widget = forms.FileInput(attrs={"name": "images", "multiple": "multiple"})
