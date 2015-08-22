from django.db import models
import lxml
from lxml.html import fromstring
import requests


# Create your models here.
class expandedurl(models.Model):
    destination_url = models.URLField(default='')
    short_url = models.URLField(default='http://')
    http_status_code = models.IntegerField(default=0)
    page_title = models.CharField(max_length=100)
    screen_capture = models.URLField(default='http://')

    def publish(self):
        if str(self.short_url).startswith('http://'):
            response = requests.get(self.short_url)
        else:
            response = requests.get('http://' + self.short_url)
        self.destination_url = response.url
        self.http_status_code = response.status_code
        siteTree = fromstring(response.content)
        self.page_title = siteTree.findtext('.//title')
        self.save()

    def __str__(self):
        return self.page_title