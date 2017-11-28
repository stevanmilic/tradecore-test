from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from socialnetwork import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'posts', views.PostViewSet)

# Login and logout views for the browsable API

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/', obtain_jwt_token),
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
