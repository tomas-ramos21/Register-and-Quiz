import csv
import io
import os
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .utils import register_lecturer
from django.conf import settings

def admin_home(request):
	admin_dict = {'name_header':'Rodney',
		      'name_menu': 'Rodney'}
	return render(request, 'administrative/admin_home.html', admin_dict)

def acc_management(request):
	acc_dict = {'name_header':'Rodney',
		    'name_menu':'Rodney'}
	return render(request, 'administrative/accountM.html', acc_dict)

def unit_management(request):
	unit_dict = {'name_header':'Rodney',
		     'name_menu':'Rodney'}
	return render(request, 'administrative/unitsM.html', unit_dict)

def space_management(request):
	space_dict = {'name_header':'Rodney',
		      'name_menu':'Rodney'}
	return render(request, 'administrative/teachingspace.html', space_dict)

def lecturer_creation(request):
	lect_dict = {'name_header': 'Rodney',
				 'name_menu': 'Rodney'}

	if request.method == "GET":
		return render(request, 'administrative/lectAccAdd.html', lect_dict)

	# Process to obtain CSV
	if request.method == "POST":
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_lecturer(file_path)

	return render(request, 'administrative/lectAccAdd.html', lect_dict)

def student_creation(request):
	student_dict = {'name_header': 'Rodney',
					'name_menu': 'Rodney'}

	# Process to render the page
	if request.method == "GET":
		return render(request, 'administrative/stuAccAdd.html', student_dict)

	# Process to obtain CSV
	if request.method == "POST":
		csv_file = request.FILES['files']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		uploaded_file_url = fs.url(filename)

	return render(request, 'administrative/stuAccAdd.html', student_dict)
