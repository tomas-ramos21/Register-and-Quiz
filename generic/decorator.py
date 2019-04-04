from administrative.models import Employee
from student.models import Student
from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

def is_student(func):
	@wraps(func)
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		std = Student.objects.filter(user=user)
		if std.exists():
			return func(request, *args, **kwargs)
		else:
			emp = Employee.objects.filter(user=user)
			if emp.exists():
				position = emp.first().pstn.upper()
				if position == 'LECTURER' or position == 'COORDINATOR':
					return redirect('lecturer:lect_error')
				else:
					return redirect('administrative:admin_error')
			else:
				return redirect('login:user_login')
	return wrapper_func

def is_lecturer(func):
	@wraps(func)
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		std = Student.objects.filter(user=user)
		if std.exists():
			return redirect('student:student_error')
		else:
			emp = Employee.objects.filter(user=user)
			if emp.exists():
				position = emp.first().pstn.upper()
				if position == 'LECTURER' or position == 'COORDINATOR':
					return func(request, *args, **kwargs)
				else:
					return redirect('administrative:admin_error')
			else:
				return redirect('login:user_login')
	return wrapper_func

def is_admin(func):
	@wraps(func)
	def wrapper_func(request, *args, **kwargs):
		user = request.user
		std = Student.objects.filter(user=user)
		if std.exists():
			return redirect('student:student_error')
		else:
			emp = Employee.objects.filter(user=user)
			if emp.exists():
				position = emp.first().pstn.upper()
				if position == 'LECTURER' or position == 'COORDINATOR':
					return redirect(reverse('lecturer:lect_error'))
				else:
					return func(request, *args, **kwargs)
			else:
				return redirect('login:user_login')
	return wrapper_func
