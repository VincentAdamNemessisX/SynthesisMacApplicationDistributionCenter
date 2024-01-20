"""SynthesisMacApplicationDistributionCenter URL Configuration

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
from typing import List, Any

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import RedirectView
from django.views.static import serve
from django_router import router
from analytics.views import index as ana
from announcements.views import *
from testunit.views import *
from software.views import *
from category.views import *
from comments_with_articles.views import *

urlpatterns = [
                  re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
                  url(r'^favicon.ico$', RedirectView.as_view(url=r'/static/favicon.ico')),
                  path('center/all/control/', admin.site.urls),
                  path('', index),
                  path('index/', index),
                  path('generic/', generic),
                  path('help/', help),
                  path('elements/', elements),
                  path('analytics/', ana),
                  # path('category/', category),
                  path('software_details/', software_details),
                  path('publish/', publish_article_and_software_page),
                  path('temp/', temp),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + router.urlpatterns
document_root = settings.STATIC_ROOT
