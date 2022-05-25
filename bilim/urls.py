"""bilim URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from authorize.urls import router as auth_router
from university.urls import router as university_router
from tasker.urls import router as tasker_router
from bilim import settings

router = DefaultRouter()
router.registry.extend(auth_router.registry)
router.registry.extend(university_router.registry)
router.registry.extend(tasker_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authorize.urls')),
    path('api/', include(router.urls))
]
urlpatterns += staticfiles_urlpatterns('static')
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
