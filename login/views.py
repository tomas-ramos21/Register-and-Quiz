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
from generic.utils import get_context

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
				user_dict = get_context(curr_user)
				if username[:3] == '333':
					return HttpResponseRedirect(reverse('student:student_index'))
				elif username[:3] == '456':
					return render(request, 'Lecturer/Lecturer.html', user_dict)
				elif username[:3] == '789' or username == 'admin':
					return render(request, 'administrative/admin_home.html', user_dict)
				else:
					return HttpResponse("Invalid account")
			else:
				return HttpResponse("Account Not Active")   # Need proper error page.
		else:
			return HttpResponse("Invalid Login Details.")   # Need proper error page.
	else:
		return render(request, 'login/index.html')
