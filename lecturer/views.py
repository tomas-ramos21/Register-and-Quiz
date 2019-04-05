import os
import re
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from generic.utils import register_questions, publish_question, register_class, add_students, register_topics, get_lecturer_context, is_expired
from generic.graphs import answer_graph
from django.conf import settings
from administrative.models import Unit, Employee, Teaching_Period, Room
from lecturer.models import Class, Question, Topic, Teaching_Day, Published_Question
from lecturer.forms import classForm
from datetime import datetime
from generic.decorator import is_lecturer
from generic.graphs import admin_attendance_graph
from django.contrib import messages
from datetime import datetime, timezone, timedelta

@login_required
@is_lecturer
def lect_home(request):
	user = request.user
	user_dict = get_lecturer_context(user)
	return render(request, 'Lecturer/lecturerHome.html', user_dict)

@login_required
@is_lecturer
def lect_publish(request, q_id, topic_id, period_id):

	user = request.user
	question = Question.objects.filter(id=q_id).first()
	topic = Topic.objects.filter(id=topic_id).first()
	period = Teaching_Period.objects.filter(id=period_id).first()

	user_dict = get_lecturer_context(user)
	user_dict['question_title'] = question.title

	if request.method == "POST":
		time = request.POST.get('max_time')
		class_code = request.POST.get('current_class')
		room = request.POST.get('current_room')
		room = Room.objects.filter(id=room).first()
		curr_class = Class.objects.filter(unit_id=topic.unit_id).filter(t_period=period).filter(code=class_code).first()
		if curr_class is not None:
			if Teaching_Day.objects.filter(c_id=curr_class).filter(date_td=datetime.utcnow().date()).first() is None:
				t_day = Teaching_Day(r_id=room, c_id=curr_class)
				t_day.save()

			code, question_item = publish_question(question, time, curr_class)
			
			request.session['question_data'] = question_item.code

			return redirect('lecturer:lect_project')
		else:
			return redirect('lecturer:lect_error')

	return render(request, "Lecturer/LecturerPublish.html", user_dict)

@login_required
@is_lecturer
def lect_project(request):
	user = request.user
	user_context = get_lecturer_context(user)
	context = request.session.get('question_data')
	if context is not None:
		pub_qn = Published_Question.objects.filter(code=context).first()
		if pub_qn is not None:
			if is_expired(pub_qn):
				return redirect('lecturer:lect_error')
			else:
				code = str(pub_qn.code)
				code = code[:3] + ' - ' + code[3:6] + ' - ' + code[6:9]
				
				# Calculating remaining time 
				time_passed = datetime.now(timezone.utc) - pub_qn.tm_stmp
				seconds_passed = time_passed.total_seconds()
				seconds_remaining = pub_qn.minutes_limit * 60 - seconds_passed
				
				context2 = {
					'rem_time' : seconds_remaining,
					't_num' : pub_qn.question.topic_id.number,
					't_name' : pub_qn.question.topic_id.name,
					'text' : pub_qn.question.text,
					'code' : code,
				}
				user_dict = user_context.copy()
				user_dict.update(context2)
				return render(request, "Lecturer/lecturerProject.html", user_dict)
		else:
			return redirect('lecturer:lect_error')
	else:
		return redirect('lecturer:lect_error')

@login_required
@is_lecturer
def lect_units(request, unit_code):
	user = request.user
	empl = Employee.objects.filter(user=user).first()
	unit = Unit.objects.filter(code=unit_code).first()

	if unit is not None :
		topic_list = Topic.objects.filter(unit_id=unit).order_by('number')

		question_list = []
		for x in topic_list:
			query = Question.objects.filter(topic_id=x)
			for y in query:
				question_list.append(y)

		t_period = Class.objects.filter(unit_id=unit, staff_id=empl).first().t_period

		user_dict = get_lecturer_context(user)
		user_dict['unit_code'] = unit.code
		user_dict['unit_title'] = unit.title
		user_dict['question_list'] = question_list
		user_dict['topic_list'] = topic_list
		user_dict['t_period'] = t_period

		if request.method == 'POST' and 'topic_file' in request.FILES:
			csv_file = request.FILES['topic_file']
			fs = FileSystemStorage()
			filename = fs.save(csv_file.name, csv_file)
			file_path = os.path.join(settings.MEDIA_ROOT, filename)
			status, msg = register_topics(file_path)
			if status == False:
				messages.error(request, msg, extra_tags='alert-warning')
				return render(request, 'error_page.html', user_dict)

		if request.method == 'POST' and 'question_file' in request.FILES:
			csv_file = request.FILES['question_file']
			fs = FileSystemStorage()
			filename = fs.save(csv_file.name, csv_file)
			file_path = os.path.join(settings.MEDIA_ROOT, filename)
			status, msg = register_questions( file_path)
			if status == False:
				messages.error(request, msg, extra_tags='alert-warning')
				return render(request, 'error_page.html', user_dict)

		return render(request, "Lecturer/LecturerUnits.html", user_dict)
	else:
		return redirect('lecturer:lect_error')

@login_required
@is_lecturer
def lect_class(request):
	user = request.user
	user_dict = get_lecturer_context(user)

	if request.method == "POST":
		if 'student_file' in request.FILES:
			csv_file = request.FILES['student_file']
			fs = FileSystemStorage()
			filename = fs.save(csv_file.name, csv_file)
			file_path = os.path.join(settings.MEDIA_ROOT, filename)
			user = request.user
			status, msg = add_students(user, file_path)
			if status == False:
				messages.error(request, msg, extra_tags='alert-warning')
				return redirect('lecturer:lect_class')
			else:
				messages.success(request, 'Student records updated.', extra_tags='alert-warning')
				return redirect('lecturer:lect_class')
		else:
			form = classForm(request.user, request.POST)
			if form.is_valid():
				data = form.cleaned_data
				unit = data.get('unit_id')
				period = data.get('t_period')
				time_commi2 = data.get('time_commi')
				code = data.get('code')
				cl = Class.objects.filter(unit_id=unit, t_period=period, time_commi=time_commi2, code=code)
				if cl.exists():
					messages.error(request, 'Class has existed', extra_tags='alert-warning')
					return redirect('lecturer:lect_class')
				else:
					emp = Employee.objects.filter(user=user).first()
					new_class = Class(unit_id=unit, t_period=period, staff_id=emp, time_commi=time_commi2, code=code)
					new_class.save()
					msg = 'Class ' + unit.code + code + ' was created successfully.'
					messages.success(request, msg, extra_tags='alert-warning')
					return redirect('lecturer:lect_class')
			else:
				messages.error(request, 'Invalid form', extra_tags='alert-warning')
				return redirect('lecturer:lect_class')
	else:
		form = classForm(request.user)
		user_dict['form'] = form
		return render(request, "Lecturer/lecturerClass.html", user_dict)

@login_required
@is_lecturer
def lect_q_stats(request, published_id):
	user = request.user
	code = int(re.sub('[^0-9]', '', published_id))
	
	pub_qn = Published_Question.objects.filter(code=code).first()
	
	if pub_qn is not None:
		time_passed = datetime.now(timezone.utc) - pub_qn.tm_stmp
		minutes_passed = int(time_passed.total_seconds() / 60)

		if minutes_passed < pub_qn.minutes_limit:
			pub_qn.minutes_limit = minutes_passed
			pub_qn.save()
		
		request.session['question_data'] = None
		
		user_dict = get_lecturer_context(user)
		
		context = {
			'graph' : answer_graph(code),
			'ans1' : pub_qn.question.ans_1,
			'ans2' : pub_qn.question.ans_2,
			'ans3' : pub_qn.question.ans_3,
			'ans4' : pub_qn.question.ans_4,
			'q_title' : pub_qn.question.title,
			'q_text' : pub_qn.question.text,
			't_num' : pub_qn.question.topic_id.number,
			't_name' : pub_qn.question.topic_id.name,
		}
		
		user_dict.update(context)
		
		return render(request, 'Lecturer/lecturerQuesStats.html', user_dict)
	else:
		return redirect('lecturer:lect_error')

@login_required
@is_lecturer
def lect_stats(request, unit_t, period_id):
	user = request.user
	user_dict = get_lecturer_context(user)

	unit = Unit.objects.filter(code=unit_t).first()
	if unit is not None:
		period = ''
		for letter in period_id.upper():
			if letter == ',':
				letter = '-'
			elif letter == ' ':
				continue
			period += letter
		period = Teaching_Period.objects.filter(id=period).first()
		if period is not None:
			emp = Employee.objects.filter(user=user).first()
			class_item = Class.objects.filter(unit_id=unit, t_period=period, staff_id=emp)

			if class_item.exists():
				user_dict['unit'] = unit_t
				user_dict['period'] = period_id
				if request.method == 'POST':
					if request.POST.get('submit'):
						code = request.POST.get('selection')
						graph = admin_attendance_graph(period, 'class', code)
						if graph == False:
							messages.error(request, 'Information provided is wrong or the request object does not exists.',
										   extra_tags='alert-warning')
							return redirect('lecturer:lect_stats', unit_t=unit_t, period_id=period_id)
						user_dict['code'] = code
						user_dict['graph'] = graph
						return render(request, 'lecturer/statisticsAttendance.html', user_dict)
					elif request.POST.get('download'):
						response = admin_attendance_csv(period, 'class', selection)
						if response == False:
							messages.error(request, 'Information provided is wrong or the request object does not exists.',
										   extra_tags='alert-warning')
							return redirect('lecturer:lect_stats')
						return response
			else:
				messages.error(request, 'Information provided is wrong or the request object does not exists.',
										   extra_tags='alert-warning')
				return redirect('lecturer:lect_stats')
		else:
			messages.error(request, 'Information provided is wrong or the request object does not exists.',
						   extra_tags='alert-warning')
			return redirect('lecturer:lect_stats')
	else:
		messages.error(request, 'Information provided is wrong or the request object does not exists.',
										   extra_tags='alert-warning')
		return redirect('lecturer:lect_stats')
				
	return render(request, 'Lecturer/statisticsAttendance.html', user_dict)

@login_required
@is_lecturer
def lect_error(request):
	user = request.user
	user_dict = get_lecturer_context(user)
	user_dict['msg'] = 'ERROR 404' 
	user_dict['desc'] = 'Page not found'
	return render(request, 'Lecturer/error.html', user_dict)

@login_required
@is_lecturer
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
	return HttpResponseRedirect(reverse('lecturer:user_logout'))
