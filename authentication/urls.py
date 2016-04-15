from authentication.views import AccountViewSet
from django.conf.urls import url, include, patterns
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'accounts', AccountViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls))


)
