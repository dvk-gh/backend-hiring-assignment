from .views import PhotoViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', PhotoViewSet)
router.register(r'<int:pk>/', PhotoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]