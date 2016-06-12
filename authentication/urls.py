from authentication import views
from django.conf.urls import url, include, patterns
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'accounts', views.AccountViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^auth/login_view/$', views.login_view, name='login_view'),
#    url(r'^auth/login_user/$', views.login_user, name='login_user'),
    url(r'^auth/logout_user/$', views.logout_user, name='logout_user'),
    url(r'^auth/profile/(?P<pk>[0-9]+)/$', views.profile, name='profile_detail'),
#    url(r'^auth/profile/(?P<pk>[0-9]+)/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^auth/profile/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='base_login', kwargs={'template_name': 'blog/login_view.html'}),
    url(r'^accounts/sign_up/$', views.sign_up, name='sign_up', ),
    url(r'^sign_up_ok/$', TemplateView.as_view(template_name='blog/sign_up_ok.html'), name='sign_up_ok'),  ##for just rendering HTML page

#    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='base_logout',),
    #url(r'^account/logout/$', views.subComment_remove, name='subComment_remove')



)
