from rest_framework.routers import DefaultRouter
from django.urls import path, include

from authorize.views import TestView, TestViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'testviewset', TestViewSet, basename='test')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('testview/', TestView.as_view(), name='testapi'),
    path('', include(router.urls))
]
