from django import forms
from django.contrib.auth.models import User
from login.models import Employee, Student


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	id = forms.IntegerField()
	class Meta():
		model = Employee
		fields= ('id', 'password')
