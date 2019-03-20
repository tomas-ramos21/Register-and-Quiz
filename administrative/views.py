# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Tomas Ramos
# Last Modified Date: 20-03-2019


# TODO:
# 1. Discard the need for a default name argument when possible.

import csv
import io
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import register_employee, register_student
from django.conf import settings

def admin_home(request, name:str= 'Rodney') -> None:
	"""
		Renders administratives' staff home page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.

		name: Staff's name.
			String with the staff's name.
	"""
	user_dict = {'name_header': name, 'name_menu': name}
	return render(request, 'administrative/admin_home.html', user_dict)

def acc_management(request, name:str= 'Rodney') -> None:
	"""
		Renders the account management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""

	user_dict = {'name_header': name, 'name_menu': name}
	return render(request, 'administrative/accountM.html', user_dict)

def unit_management(request, name:str= 'Rodney') -> None:
	"""
		Renders the unit management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""

	user_dict = {'name_header': name, 'name_menu':name}
	return render(request, 'administrative/unitsM.html', user_dict)

def space_management(request, name:str= 'Rodney') -> None:
	"""
		Renders the space management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with teh staff's name.
	"""

	user_dict = {'name_header': name, 'name_menu': name}
	return render(request, 'administrative/teachingspace.html', user_dict)

def lecturer_creation(request, name:str= 'Rodney') -> None:
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

	user_dict = {'name_header': name, 'name_menu': name}

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

def student_creation(request, name:str= 'Rodney') -> None:
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

	user_dict = {'name_header': name, 'name_menu': name}

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
