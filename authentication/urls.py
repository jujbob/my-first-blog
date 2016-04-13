from authentication.views import AccountViewSet
from django.conf.urls import url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'accounts', AccountViewSet, base_name='account')

urlpatterns = [

    url(r'^api/', include(router.urls))


]
