from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,OrderViewSet,RouteViewSet,StopViewSet

router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'routes',RouteViewSet)
router.register(r'stops',StopViewSet)


urlpatterns = [
    path('',include(router.urls)),
]