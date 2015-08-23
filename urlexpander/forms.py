
from django import forms
from .models import expandedurl
from selenium import webdriver
import requests
import boto3
from boto3.session import Session
import botocore.session
import botocore
import os
from lab1site.settings import AWS_STORAGE_BUCKET_NAME, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID


class ExpandedUrlForm(forms.ModelForm):
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
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
        client = session.resource('s3')
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull) # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get(str(url.destination_url))
        url.page_title = driver.title
        filepath = '/tmp/' + str(url.id) + '.png'
        s3path = 'captures/' + str(url.id) + '.png'
        driver.save_screenshot(filepath)
        data = open(filepath, 'rb') # save a screenshot to disk
        client.Object(AWS_STORAGE_BUCKET_NAME, s3path).put(Body=data) #upload_file(filepath, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID)
        url.screen_capture = 'https://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME + '/' + s3path
        driver.service.process.kill()
        os.remove(filepath)
        return url