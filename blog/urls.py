from django.conf.urls import url, include, patterns
from . import views
from rest_framework import routers

## for rest API ##
router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet, base_name='post')
router.register(r'comments', views.CommentViewSet, base_name='comment')
router.register(r'subComments', views.SubCommentViewSet, base_name='subComment')

urlpatterns = patterns(

    ## for rest API ##
    '',
    url(r'^api/', include(router.urls)),

    ## for web pages ##

    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/list/', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>[0-9]+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>[0-9]+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^errors/$', views.errors, name='errors'),
    url(r'^post/(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/subComment/$', views.add_subComment_to_post, name='add_subComment_to_post'),
    url(r'^subComment/(?P<pk>\d+)/remove/$', views.subComment_remove, name='subComment_remove')

)
