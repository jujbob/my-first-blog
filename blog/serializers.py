from django.contrib.auth.models import User
from blog.models import Post, Comment
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('url', 'author', 'title', 'text', 'created_date', 'published_date', 'comments')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'url', 'author', 'text', 'created_date', 'approved_comment')
