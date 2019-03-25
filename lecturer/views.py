import os
from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from generic.utils import register_questions, publish_question
from django.conf import settings
from administrative.models import Employee
from lecturer.models import Class

def lect_home(request):
	user = request.user
	lect = Employee.objects.filter(user=user).first()

	if lect is not None:
		class_taught = Class.objects.filter(staff_id=lect)
		unit_list = [x.unit_id for x in class_taught]

		period_display = []
		t_period = [x.t_period.id.lower() for x in class_taught]
		for y in t_period:
			period = ''
			for letter in y:
				if letter == '-':
					letter = ', '
				period += letter
			period_display.append(period)

		class_display = zip(unit_list, period_display)
		user_dict = {
		'f_name' : user.first_name,
		'fl_name' : user.first_name + ' ' + user.last_name,
		'class_display' : class_display,
		}
		return render(request, 'Lecturer/lecturerHome.html', user_dict)
	else:
		return HttpResponse('Unexpected error')

def lect_publish(request):
	user = request.user
	user_dict = {'name_header': user.first_name,
				 'name_menu': user.first_name + ' ' + user.last_name}

	time = request.POST.get('max_time')
	if not time is None:
		publish_question(question, time) # NEED TO ADD THE QUESTION
										 # RENDER THE QUESTION PAGE
	return render(request, "Lecturer/LecturerPublish.html", user_dict)

def lect_units(request):
	user = request.user
	user_dict = {'f_name': user.first_name,
				 'fl_name': user.first_name + ' ' + user.last_name}

	if request.method == 'POST' and 'question_file' in request.FILES:
		csv_file = request.FILES['question_file']
		fs = FileSystemStorage()
		filename = fs.save(csv_file.name, csv_file)
		file_path = os.path.join(settings.MEDIA_ROOT, filename)
		register_questions(file_path)

	return render(request, "Lecturer/LecturerUnits.html", user_dict)

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
