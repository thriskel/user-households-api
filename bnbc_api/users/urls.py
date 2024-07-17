from django.urls import path, include
from . import views as users_views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', users_views.UserViewSet)


urlpatterns = [
    path('', include(router.urls), name='users'),
]
