from django import forms
from django.forms import ModelForm
from . import models

class classForm(ModelForm):
    class Meta:
        fields = ['unit_id', 't_period', 'time_commi', 'code']
        model = models.Class
        