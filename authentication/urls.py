from authentication import views
from django.conf.urls import url, include, patterns
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'accounts', views.AccountViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^auth/login_view/$', views.login_view, name='login_view'),
    url(r'^auth/login_user/$', views.login_user, name='login_user'),
#    url(r'^account/login/?*$', views.login_user, name='login_user'),
    url(r'^auth/logout_user/$', views.logout_user, name='logout_user')
    #url(r'^account/logout/$', views.subComment_remove, name='subComment_remove')



)
