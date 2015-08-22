"""lab1site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, patterns
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.urls_list, name='urls_list'),
    url(r'^url/(?P<pk>[0-9]+)/$', views.urls_detail, name='urls_detail'),
    url(r'^url/new/$', views.url_new, name='url_new'),
    url(r'^url/(?P<pk>[0-9]+)/edit/$', views.url_edit, name='url_edit'),
    url(r'^url/(?P<pk>[0-9]+)/remove/$', views.url_remove, name='url_remove'),
    url(r'^urlsapi/$', views.UrlList.as_view()),
    #url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)