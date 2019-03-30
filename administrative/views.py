# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Tomas Ramos
# Last Modified Date: 23-03-2019

import csv
import io
import os
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from generic.utils import register_employee, register_student, find_user, register_room, register_building, find_room, find_building, register_units, register_courses, register_teaching_period, extract_info_student, extract_info_lecturer
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from student.models import Student
from administrative.models import Employee
from generic.utils import get_admin_context

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
	user_dict = get_admin_context(user)
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
	user_dict = get_admin_context(user)
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
	user_dict = get_admin_context(user)

	if request.method == 'GET':
		return render(request, 'administrative/unitsM.html', user_dict)

	if request.method == 'POST':
		radio		= request.POST.get('add/remove')
		unit_code	= request.POST.get('unit')
		unit_title	= request.POST.get('unitTitle')
		acc_type	= request.POST.get('Accounts')
		username	= request.POST.get('username')
		info_tuple 	= (radio, unit_code, unit_title, acc_type, username)
		if None in info_tuple: # If information is incomplete3
			pass
		user, obj_type = find_user(username)

	if request.method == 'POST':
		username = request.POST.get('search_user')
		if username is None:
			pass
		else:
			user, obj_type = find_user(username)

	if request.method == "POST" and 'units_file' in request.FILES:
		csv_file = request.FILES['units_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_units(file_path)

	if request.method == "POST" and 'courses_file' in request.FILES:
		csv_file = request.FILES['courses_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_courses(file_path)

	if request.method == "POST" and 'teaching_period_file' in request.FILES:
		csv_file = request.FILES['teaching_period_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_teaching_period(file_path)

	return render(request, 'administrative/unitsM.html', user_dict)

def space_management(request):
	"""
		Renders the space management options page.

		Parameters
		----------
		request: HTTP request object
			Contains the request type sent by the user.

		name: Staff's name
			String with the staff's name.
	"""
	user = request.user
	user_dict = get_admin_context(user)

	# Re-render the page
	if request.method == "GET":
		return render(request, 'administrative/teachingspace.html', user_dict)


	# Process to obtain CSV - Rooms
	if request.method == "POST" and 'room_file' in request.FILES:
		csv_file = request.FILES['room_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_room(file_path)

	# Process to obtain CSV - Buildings
	if request.method == "POST" and 'building_file' in request.FILES:
		csv_file = request.FILES['building_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_building(file_path)

	# Process to find Rooms
	if request.method == "POST" and not request.POST.get('room_code') is None:
		room_code = request.POST.get('room_code')
		room = find_room(room_code)

	# Process to find Buildings
	if request.method == "POST" and not request.POST.get('building_code') is None:
		building_code = request.POST.get('building_code')
		building = find_building(building_code)

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
			String with the staff's name.
	"""
	user = request.user
	user_dict = get_admin_context(user)
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
			String with the staff's name.
	"""
	user = request.user
	user_dict = get_admin_context(user)

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

def attendance_stats(request):
	user = request.user
	user_dict = get_admin_context(user)
	return render(request, 'administrative/statistics.html', user_dict)

def user_view(request):
	user = request.user
	username = request.POST.get('search_user')
	searched_user = User.objects.get(username=username)

	if searched_user is None:
		return HttpResponse('User does not exist.')

	student = Student.objects.filter(user=searched_user).first()
	lecturer = Employee.objects.filter(user=searched_user).first()

	classes = None
	units = None
	courses = None
	user_object = None
	if student is not None:
		classes, courses, units = extract_info_student(student)
		user_object = student
	else:
		classes, units = extract_info_lecturer(lecturer)
		user_object = lecturer

	user_dict = get_admin_context(user)
	user_dict['user_object'] = user_object
	user_dict['classes'] = classes
	user_dict['units'] = units
	user_dict['courses'] = courses

	return render(request, 'administrative/userView.html', user_dict)

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
