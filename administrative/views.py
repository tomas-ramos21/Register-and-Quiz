# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Tomas Ramos
# Last Modified Date: 23-03-2019

import csv
import io
import os
from django.shortcuts import render
from login.models import Student, Employee
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from generic.utils import register_employee, register_student
from django.contrib.auth.decorators import login_required
from django.conf import settings

def admin_home(request):
	"""
		Renders administratives' staff home page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.

		name: Staff's name.
			String with the staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	return render(request, 'administrative/admin_home.html', user_dict)

def acc_management(request):
	"""
		Renders the account management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	return render(request, 'administrative/accountM.html', user_dict)

def unit_management(request):
	"""
		Renders the unit management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}

	if request.method == 'GET':
		return render(request, 'administrative/unitsM.html', user_dict)

	if request.method == 'POST':
		radio		= request.POST.get('add/remove')
		unit_code	= request.POST.get('unit')
		unit_title	= request.POST.get('unitTitle')
		acc_type	= request.POST.get('Accounts')
		username	= request.POST.get('username')
		info_tuple 	= (radio, unit_code, unit_title, acc_type, username)
		if None in info_tuple: # If information is incomplete
			pass

	if request.method == 'POST':
		username	= request.POST.get('search_user')


	return render(request, 'administrative/unitsM.html', user_dict)

def space_management(request):
	"""
		Renders the space management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}

	return render(request, 'administrative/teachingspace.html', user_dict)

def employee_creation(request):
	"""
		Handles request sent by the user when using the
		staff creation page. The page may be re-rendered or
		a file may be submitted.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}
	# Re-render the page
	if request.method == "GET":
		return render(request, 'administrative/lectAccAdd.html', user_dict)

	# Process to obtain CSV & create accounts
	if request.method == "POST":
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_employee(file_path)

	return render(request, 'administrative/lectAccAdd.html', user_dict)

def student_creation(request):
	"""
		Handles request sent by the user when using the
		staff creation page. The page may be re-rendered or
		a file may be submitted.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}

	# Process to render the page
	if request.method == "GET":
		return render(request, 'administrative/stuAccAdd.html', user_dict)

	# Process to obtain CSV & create accounts
	if request.method == "POST":
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_student(file_path)
	return render(request, 'administrative/stuAccAdd.html', user_dict)

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
    return HttpResponseRedirect(reverse('administrative:user_logout'))
