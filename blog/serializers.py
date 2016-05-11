from blog.models import Post, Comment, SubComment
from rest_framework import serializers


#class UserSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = User
#        fields = ('url', 'username', 'email')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Post
        fields = ('url', 'author', 'title', 'text', 'created_date', 'published_date', 'comments')
        read_only_fields = ('author', 'comments')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'post', 'author', 'text', 'created_date', 'approved_comment')
        read_only_fields = ('author',)

class SubCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SubComment
        fields = ('url', 'post', 'comment', 'author', 'text', 'created_date')
        read_only_fields = ('post', 'comment', 'author',)
