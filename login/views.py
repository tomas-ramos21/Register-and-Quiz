# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Log user into the website.
# Last Modified By: Madyarini Grace Ariel
# Last Modified Date: 20-03-2019

# TODO
# 1. Add HTML error pages, and redirect user there in case of bad logins.
# 2. Check naming conventions that be used for redirections.

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from administrative.models import Employee
from student.models import Student
from django.contrib import messages

def index(request):
	"""
		Renders the login page of the website.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	return HttpResponseRedirect(reverse('login:user_login'))

def user_login(request):
	"""
		Collects user login details, and authenticates
		them. According to their user type (e.g. Student),
		they are redirected to the according page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""

	if request.method == 'POST':

		# Collect user info
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Autenticate user
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				curr_user = User.objects.filter(username=username).first()
				if user.username == 'admin':
					return HttpResponseRedirect(reverse('administrative:admin_home'))

				emp = Employee.objects.filter(user=curr_user).first()
				if emp is not None:
					position = emp.pstn.upper()
					if position == 'LECTURER' or position == 'UNIT COORDINATOR':
						return HttpResponseRedirect(reverse('lecturer:lect_home'))
					else:
						return HttpResponseRedirect(reverse('administrative:admin_home'))
				else:
					std = Student.objects.filter(user=curr_user).first()
					if std is not None:
						return HttpResponseRedirect(reverse('student:student_index'))
					else:
						messages.error(request, 'Invalid account type', extra_tags='alert-warning')  
						return redirect('login:user_login')
			else:
				messages.error(request, 'Account is inactive.', extra_tags='alert-warning')  
				return redirect('login:user_login')
		else:
			messages.error(request, 'Invalid login details', extra_tags='alert-warning')  
			return redirect('login:user_login')
	else:
		return render(request, 'login/index.html')
