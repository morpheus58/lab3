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


# Create your views here.
@login_required(login_url='accounts/login')
def urls_list(request):
    expandedurls = expandedurl.objects.all()
    return render(request, 'urlexpander/urls_list.html', {'expandedurls': expandedurls})
@login_required(login_url='/lab1/accounts/login')
def urls_detail(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    return render(request, 'urlexpander/urls_detail.html', {'expandedurl': url})

@login_required(login_url='accounts/login')
def url_new(request):
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST)
        if form.is_valid():
            eurl = form.save(commit=False)
            site = requests.get(eurl.short_url)
            eurl.http_status_code = site.status_code
            eurl.destination_url = site.url
            siteTree = fromstring(site.content)
            eurl.page_title = siteTree.findtext('.//title')
            eurl.save()
            return redirect('urlexpander.views.urls_detail', pk=eurl.pk)
    else:
        form = ExpandedUrlForm()
        return render(request, 'urlexpander/urls_edit.html', {'form': form})
@login_required(login_url='accounts/login')
def url_edit(request, pk):
    url = get_object_or_404(expandedurl, pk=pk)
    if request.method == "POST":
        form=ExpandedUrlForm(request.POST, instance=url)
        if form.is_valid():
            url = form.save(commit=False)
            site = requests.get(url.short_url)
            url.http_status_code = site.status_code
            url.destination_url = site.url
            siteTree = fromstring(site.content)
            url.page_title = siteTree.findtext('.//title')
            url.save()
            return redirect('urlexpander.views.urls_detail', pk=url.pk)
    else:
        form = ExpandedUrlForm(instance=url)
        return render(request, 'urlexpander/urls_edit.html', {'form': form})

@login_required(login_url='accounts/login')
def url_remove(request, pk):
  url = get_object_or_404(expandedurl, pk=pk)
  url.delete()
  return urls_list(request)

class UrlList(APIView):
    def get(self, request, format=None):
        urls = expandedurl.objects.all().order_by('page_title')
        serializer = ExpandedUrlSerializer(urls, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ExpandedUrlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @login_required(login_url='lab1/accounts/login')
# def user_list(request):
#  if not request.user.is_authenticated():
#     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
#  else:
#     users = Users.objects.all()
#     return render(request, 'urlexpander/user_list.html', {'users': users})

