"""gpapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from agenda import views as agenda_views
from user import views as user_views


router = routers.DefaultRouter()
router.register('agendas', agenda_views.AgendaViewSet, base_name='agendas')
router.register('users', user_views.UserViewSet)

urlpatterns = [
    url('', include(router.urls)),
    url('api/', include(router.urls)),

    path('admin/', admin.site.urls),
    path('browserable-api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
]
