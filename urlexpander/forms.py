
from django import forms
from .models import expandedurl
from selenium import webdriver
import requests
import boto3
import os
from lab1site.settings import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID


class ExpandedUrlForm(forms.ModelForm):
    short_url = forms.URLField()
    class Meta:
        model = expandedurl
        fields = ('short_url',)
    def save(self, commit=True):
        short_url_data = self.data.get('short_url')
        url = expandedurl.objects.create()
        url.short_url = short_url_data
        site = requests.get(short_url_data)
        url.http_status_code = site.status_code
        url.destination_url = site.url
        client = boto3.resource('s3')
        driver = webdriver.PhantomJS() # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get(str(url.destination_url))
        url.page_title = driver.title
        filepath = '/tmp/' + str(url.id) + '.png'
        s3path = 'captures/' + str(url.id) + '.png'
        driver.save_screenshot(filepath)
        data = open(filepath, 'rb') # save a screenshot to disk
        client.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=s3path, Body=data) #upload_file(filepath, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID)
        url.screen_capture = 'https://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME + '/' + s3path
        driver.quit()
        if os.path.exists(filepath):
            os.remove(filepath)
        url.save()
        return url