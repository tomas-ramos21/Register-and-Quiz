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
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from student import views as student

def index(request):
	"""
		Renders the login page of the website.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.
	"""
	return HttpResponseRedirect(reverse('login:user_login'))

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
				curr_user = User.objects.filter(username=username).first()
				# curr_user = request.user.first_name + ' ' + request.user.last_name
				# Conditional Redirections
				if username[:3] == '333':
					return HttpResponseRedirect(reverse('student:student_index'))
					#return redirect('student:student_dashboard', args=[curr_user])
					# return student.student_dashboard(request, curr_user)
				elif username[:3] == '456':
					return render(request, 'Lecturer/Lecturer.html', curr_user)
				elif username[:3] == '789':
					return render(request, 'administrative/admin_home.html', curr_user)
				else:
					return HttpResponse("Invalid account")
			else:
				return HttpResponse("Account Not Active")   # Need proper error page.
		else:
			return HttpResponse("Invalid Login Details.")   # Need proper error page.
	else:
		return render(request, 'login/index.html')
