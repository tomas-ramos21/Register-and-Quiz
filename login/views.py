# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Log user into the website.
# Last Modified By: Tomas Ramos
# Last Modified Date: 20-03-2019

# TODO
# 1. Add HTML error pages, and redirect user there in case of bad logins.
# 2. Check naming conventions that be used for redirections.

from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout

def index(request):
	"""
		Renders the login page of the website.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	return render(request, 'login/index.html')

@login_required
def user_logout(request):
	"""
		Closes the current session of the user,
		and redirects them to the login page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	logout(request)
	return HttpResponseRedirect(reverse('index'))

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
				name = request.user.first_name + ' ' + request.user.last_name
				# Conditional Redirections
				if username[:3] == '123':
					return render(request, 'student/student.html', name)
				elif username[:3] == '456':
					return render(request, 'Lecturer/Lecturer.html', name)
				elif username[:3] == '789':
					return render(request, 'administrative/admin_home.html', name)
			else:
				return HttpResponse("Account Not Active")   # Need proper error page.
		else:
			return HttpResponse("Invalid Login Details.")   # Need proper error page.
	else:
		return render(request, 'login/index.html')
