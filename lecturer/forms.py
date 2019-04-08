from django import forms
from django.forms import ModelForm
from . import models
from lecturer.models import Class
from administrative.models import Employee, Teaching_Period

class classForm(forms.ModelForm):
    class Meta:
        fields = ['unit_id', 't_period', 'time_commi', 'code']
        model = models.Class

    def __init__(self, user, *args, **kwargs):
        super(classForm, self).__init__(*args, **kwargs)
        emp = Employee.objects.filter(user=user).first()
        self.fields['unit_id'].queryset  = emp.units.all()

class pubQnForm(forms.ModelForm):
	class Meta:
		fields = ['q_class', 'minutes_limit']
		model = models.Published_Question
	
	def __init__(self, emp, unit, period, *args, **kwargs):
		super(pubQnForm, self).__init__(*args, **kwargs)
		self.fields['q_class'].widget.attrs['placeholder'] = 'Select Class'
		self.fields['q_class'].queryset  = Class.objects.filter(staff_id=emp, unit_id=unit, t_period=period)
		self.fields['minutes_limit'].widget.attrs['placeholder'] = 'Enter time limit in minutes'
		self.fields['q_class'].widget.attrs.update({'class':'form_custom'})
		self.fields['minutes_limit'].widget.attrs.update({'class':'form_custom'})

