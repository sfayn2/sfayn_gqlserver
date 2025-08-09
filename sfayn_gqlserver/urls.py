"""sfayn_gqlserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.sites.models import Site
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import re_path
from django.views.static import serve
from ddd.order_management.presentation import django_rest_views


urlpatterns = [
     path('admin/', admin.site.urls),
     path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
     path('webhook/', include('order_management.urls'))
]


if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

admin.site.site_url = settings.VIEW_SITE_URL
try:
    admin.site.site_title = Site.objects.get_current() 
    admin.site.site_header = Site.objects.get_current() 
except:
    # django migrate will check urls.py expects to have a runtime since Site is not ready
    pass
