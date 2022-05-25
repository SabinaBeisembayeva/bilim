from rest_framework.routers import DefaultRouter
from django.urls import path, include
from university.models import Specialty

from university.views import MotivationView, UniversityView, FacultyView, SpecialtyView

router = DefaultRouter()
router.register(r'university', UniversityView, basename='university')
router.register(r'faculty', FacultyView, basename='faculty')
router.register(r'specialty', SpecialtyView, basename='specialty')
router.register(r'motivation', MotivationView, basename='motivation')


# urlpatterns = [
#     path('university/<int:uni_id>/specialty/<int:spec_id>/', SpecialtyView.as_view(), name='specialty'),
#     path('', include(router.urls))
# ]
