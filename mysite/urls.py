from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from blog import views

router = routers.DefaultRouter()
router.register(r'api/users', views.UserViewSet)
router.register(r'api/posts', views.PostViewSet)
router.register(r'api/comments', views.CommentViewSet)
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',),
                       url(r'^accounts/profile/$', 'blog.views.post_list',),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
                       url(r'', include('blog.urls')),

                       ## for rest_framework ##
                       url(r'^', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                       )