from .models import expandedurl
from .forms import ExpandedUrlForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
import lxml
from lxml.html import fromstring
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import ExpandedUrlSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ratelimit.decorators import ratelimit
from rest_framework import generics, mixins
from ratelimit.mixins import RatelimitMixin
from rest_framework.reverse import reverse

# Create your views here.
@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/lab3/accounts/login')
def urls_list(request):
    expandedurls = expandedurl.objects.all()
    return render(request, 'urlexpander/urls_list.html', {'expandedurls': expandedurls})
@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/lab3/accounts/login')
def urls_detail(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    return render(request, 'urlexpander/urls_detail.html', {'expandedurl': url})
@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/lab3/accounts/login')
def url_new(request):
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST)
        if form.is_valid():
            url = form.save()
            return redirect('urlexpander.views.urls_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'urlexpander/urls_edit.html', {'form': form})
@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='/lab3/accounts/login')
def url_edit(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST, instance=url)
        if form.is_valid():
            eurl = ExpandedUrlSerializer.update(self=url, instance=url)
            eurl.save()
            return redirect('urlexpander.views.urls_detail', pk=eurl.pk)
    else:
        form = ExpandedUrlForm(instance=url)
        return render(request, 'urlexpander/urls_edit.html', {'form': form})

@ratelimit(key='ip', rate='10/m', block=True)
@login_required(login_url='lab3/accounts/login')
def url_remove(request, pk):
  url = get_object_or_404(expandedurl, pk=pk)
  url.delete()
  return urls_list(request)


class UrlList(RatelimitMixin, generics.ListCreateAPIView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_block = True
    ratelimit_method = 'GET', 'POST'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = expandedurl.objects.all()
    serializer_class = ExpandedUrlSerializer
class UrlDetail(RatelimitMixin, generics.RetrieveUpdateDestroyAPIView):
    ratelimit_key = 'ip'
    ratelimit_rate = '10/m'
    ratelimit_block = True
    ratelimit_method = 'GET', 'POST', 'DELETE', 'PUT'
    queryset = expandedurl.objects.all().order_by('page_title')
    serializer_class = ExpandedUrlSerializer
    # def post(self, request, format=None):
    #     serializer = ExpandedUrlSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
