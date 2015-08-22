
from django import forms
from .models import expandedurl

class ExpandedUrlForm(forms.ModelForm):

    class Meta:
        model = expandedurl
        fields = ('short_url',)
