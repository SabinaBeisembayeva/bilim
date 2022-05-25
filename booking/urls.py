from rest_framework.routers import DefaultRouter
from django.urls import path, include

from booking.views import TestViewSet

router = DefaultRouter()
router.register(r'testviewset', TestViewSet, basename='test')

urlpatterns = [
    path('', include(router.urls))
]
