from rest_framework.routers import DefaultRouter
from django.urls import path, include

from booking.views import BookingView

router = DefaultRouter()
router.register(r'booking', BookingView, basename='booking')