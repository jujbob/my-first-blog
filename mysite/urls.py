from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers

router = routers.DefaultRouter()
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('blog.urls')),
                       url(r'', include('authentication.urls')),

#                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',),
#                       url(r'^accounts/profile/$', 'blog.views.post_list',),
#                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

                       ## for rest_framework ##
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                       )