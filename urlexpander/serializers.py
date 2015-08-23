__author__ = 'Morya Jr'
from rest_framework import serializers
from .models import expandedurl
from selenium import webdriver
import requests

from boto3.session import Session
import os
from lab1site.settings import AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import botocore.session
import botocore
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class ExpandedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = expandedurl
        fields = ('id', 'short_url', 'destination_url', 'http_status_code', 'page_title', 'screen_capture')
        read_only_fields = ('destination_url', 'http_status_code', 'page_title', 'screen_capture')
    def capture(self, url):
        session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
        s3 = session.resource('s3')
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull) # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get(str(url.destination_url))
        url.page_title = driver.title
        filepath = '/tmp/' + str(url.id) + '.png'
        s3path = 'captures/' + str(url.id) + '.png'
        driver.save_screenshot(filepath)
        data = open(filepath, 'rb') # save a screenshot to disk
        s3.Object(AWS_STORAGE_BUCKET_NAME, s3path).put(Body=data) #upload_file(filepath, AWS_STORAGE_BUCKET_NAME, AWS_ACCESS_KEY_ID)
        url.screen_capture = 'https://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME + '/' + s3path
        driver.service.process.kill()
        os.remove(filepath)
        return url

    def create(self, validated_data):
        short_url_data = validated_data.pop('short_url')
        url = expandedurl.objects.create()
        url.short_url = short_url_data
        site = requests.get(short_url_data)
        url.http_status_code = site.status_code
        url.destination_url = site.url
        return self.capture(url)

    def update(self, instance):
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        b = conn.get_bucket(AWS_STORAGE_BUCKET_NAME)
        k = Key(b)
        #session = botocore.session.get_session()
        #client = boto3.resource('s3')
        #client = session.create_client('s3')
        driver = webdriver.PhantomJS(service_log_path=os.path.devnull) # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get(str(instance.short_url))
        instance.page_title = driver.title
        filepath = '/tmp/' + str(instance.id) + '.png'
        k.key = 'captures/' + str(instance.id) + '.png'
        s3path = 'captures/' + str(instance.id) + '.png'
        driver.save_screenshot(filepath)
        k.set_contents_from_filename(filepath)
        k.make_public()
        driver.service.process.kill()
        #data = open(filepath, 'rb') # save a screenshot to disk
        #client.put_object(Key=s3path, Body=data, Bucket=AWS_STORAGE_BUCKET_NAME) #client.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=s3path, Body=data)
        instance.screen_capture = 'https://s3.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME + '/' + s3path
        instance.destination_url = requests.get(instance.short_url).url
        instance.save()
        driver.service.process.kill()
        #driver.quit()
        os.remove(filepath)
        return instance