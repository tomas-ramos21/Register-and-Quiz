# Author: Madyarini Grace Ariel
# Date: 23-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Madyarini Grace Ariel
# Last Modified Date: 23-03-2019

from django.urls import reverse
from django.shortcuts import render, redirect
from student.models import Student, Answer
from lecturer.models import Question, Published_Question, Teaching_Day
from administrative.models import Unit
from datetime import datetime, timedelta, timezone
from student.forms import codeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ipware import get_client_ip
from django.http import HttpResponse, HttpResponseRedirect
from lecturer.models import Class

@login_required
def student_index(request):
	"""
		Redirects to student's dashboard page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	return HttpResponseRedirect(reverse('student:student_dashboard'))

@login_required
def student_dashboard(request):
	"""
		Renders student's dashboard page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	user = request.user
	std = Student.objects.filter(user=user).first()
	
	if std is not None:
		enrolled_class = std.s_class.all()
		unit_list  = [x.unit_id for x in enrolled_class]
		
		period_display = []
		
		t_period = [x.t_period.id.lower() for x in enrolled_class]
		for y in t_period:
			period = ''
			for letter in y:
				if letter == '-':
					letter = ', '
				period += letter
			period_display.append(period)
			
		class_display = zip(unit_list, period_display)
		context = {
		'f_name' : user.first_name,
		'fl_name' : user.first_name + ' ' + user.last_name,
		'class_display' : class_display,
		}
		return render(request, 'student/student_dashboard.html', context)
	else:
		return HttpResponse('Not registered as a student')

@login_required
def student_codeinput(request):
	"""
		Renders the form for question code input.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	if request.method == 'POST':
		form = codeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			code = cd.get('code')
			item = Published_Question.objects.filter(code=code).first()
			if item is not None:
				diff = datetime.now(timezone.utc) - item.tm_stmp
				seconds_passed = diff.total_seconds()
				if seconds_passed > int(item.seconds_limit):
					return HttpResponse('Question has expired.')
				else:
					context = {
					'unit_code' : item.question.topic_id.unit_id.code,
					'unit_title' : item.question.topic_id.unit_id.title,
					'ans1' : item.question.ans_1,
					'ans2' : item.question.ans_2,
					'ans3' : item.question.ans_3,
					'ans4' : item.question.ans_4,
					'question_code' : code
					}
					request.session['question_data'] = context
					return HttpResponseRedirect(reverse('student:student_answer'))
			else:
				return HttpResponse('No matching question code.')
	else:
		form = codeForm()

	return render(request, 'student/studentInput.html', {'form':form})

@login_required
def student_answer(request):
	"""
		Renders the answer page for the student to submit answer. 

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	
	if request.method == 'POST':
		if 'choice' in request.POST:
			selection = request.POST.get('choice')
			
			# Get the student object who submitted the answer
			user = request.user
			std = Student.objects.filter(user=user).first()
			
			if std is None:
				return HttpResponse('No student found')
			
			# Get the details of the question answered
			context = request.session.get('question_data')
			question_answered = Published_Question.objects.filter(code=context['question_code']).first().question
			
			# Get the details of the Teaching Day when the question was answered
			t_period = ''
			lecturer = None
			class_item = None
			
			enrolled_class = std.s_class.all()
			for x in enrolled_class:
				if x.unit_id.code == context['unit_code']:
					class_item = x
					lecturer = x.staff_id
					break
			
			print(class_item)
			t_day = Teaching_Day.objects.filter(c_id=class_item, date_td=datetime.today()).first()
			if t_day is None:
				return HttpResponse('Unexpected error')
			
			# Get IP address of student
			client_ip, is_routable = get_client_ip(request)
			if client_ip is None:
				client_ip = '0.0.0.0'
			else:
				if is_routable:
					str = ''
					for char in client_ip:
						if char != '.' :
							str += char
						else:
							break
					if str == '10':
						ip_type = 'internal'
					else:
						ip_type = 'external'
					print(client_ip)
					print(ip_type)
				else:
					ip_type = 'private'		
					print(ip_type)
			
			# Create a new Answer object and save it to the database
			new_answer = Answer(s_id=std, q_id=question_answered, teach_day=t_day, ans=selection, tm_stmp=datetime.now(timezone.utc))
			new_answer.save()
			
			return HttpResponseRedirect(reverse('student:student_index'))
	else:
		context = request.session.get('question_data')
		if context is not None:
			return render(request, 'student/studentQuestion.html', context)
		else:
			return HttpResponseRedirect(reverse('student:student_codeinput'))

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
    return HttpResponseRedirect(reverse('login:user_login'))

