from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,OrderViewSet,RouteViewSet,StopViewSet,DriverViewSet,RouteInfoViewSet

router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'orders',OrderViewSet)
router.register(r'routes',RouteViewSet)
router.register(r'stops',StopViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'route_info',RouteInfoViewSet)

urlpatterns = [
    path('',include(router.urls)),
]