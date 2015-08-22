__author__ = 'Morya Jr'
from rest_framework import serializers
from .models import expandedurl
from selenium import webdriver
import requests


class ExpandedUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = expandedurl
        fields = ('id', 'short_url')
