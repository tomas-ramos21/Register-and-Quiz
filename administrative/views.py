# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Tomas Ramos
# Last Modified Date: 20-03-2019

import csv
import io
import os
from django.shortcuts import render
from login.models import Student, Employee
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from generic.utils import register_employee, register_student
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

def lecturer_creation(request):
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

def register_employee(csv_path: str) -> None:
    """
        Registers lecturers in the platform.

        Iterates over the rows of a CSV file
        collecting the information to be used
        for the account creation.

        Parameters
        ----------
        csv_path: str
            String containing the path to the
            file.

        TODO
        ----------
        1. Function do check the information
        used during creation is accurate.
    """

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email',
               'department',
               'position']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):  # For each row
            if idx != 0:                    # If row isn't the header
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                user = User()
                user.set_password(crt_dict['password'])
                user.username = crt_dict['id']
                user.first_name = crt_dict['first_name']
                user.last_name = crt_dict['last_name']
                user.email = crt_dict['email']
                user.save()
                employee = Employee(user=user,
                                    dpt=crt_dict['department'],
                                    pstn=crt_dict['position'])
                employee.save()

def register_student(csv_path: str) -> None:
    """
        Registers students in the platform.

        Iterates over the rows of a CSV file
        collecting the information to be used
        for the account creation.

        Parameters
        ----------
        csv_path: str
            String containing the path to the
            file.

        TODO
        ----------
        1. Function do check the information
        used during creation is accurate.
    """

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                user = User()
                user.set_password(crt_dict['password'])
                user.username = crt_dict['id']
                user.first_name = crt_dict['first_name']
                user.last_name = crt_dict['last_name']
                user.email = crt_dict['email']
                user.save()
                student = Student(user=user)
                student.save()
