# Author: Madyarini Grace Ariel
# Date: 23-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Madyarini Grace Ariel
# Last Modified Date: 23-03-2019

from django.urls import reverse
from django.shortcuts import render, redirect
from student.models import Student, Answer
from lecturer.models import Question, Published_Question, Teaching_Day, Class
from administrative.models import Unit, Teaching_Period
from datetime import datetime, timedelta, timezone
from student.forms import codeForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout
from ipware import get_client_ip
from django.http import HttpResponse, HttpResponseRedirect
from lecturer.models import Class
from generic.decorator import is_student
from generic.utils import get_std_context
from generic.graphs import attendance_graph
from django.contrib import messages

@login_required
@is_student
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
@is_student
def student_dashboard(request):
	"""
		Renders student's dashboard page.
		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	user = request.user
	user_dict = get_std_context(user)

	return render(request, 'student/student_dashboard.html', user_dict)

@login_required
@is_student
def student_codeinput(request):
	"""
		Renders the form for question code input.
		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	
	user = request.user
	user_dict = get_std_context(user)
	std = Student.objects.filter(user=user).first()
	
	if request.method == 'POST':
		form = codeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			code = cd.get('code')
			item = Published_Question.objects.filter(code=code).first()
			if item is not None: # If Published_Question exists 
				if item.q_class in std.s_class.all():
					ans = Answer.objects.filter(s_id=std, q_id=item).first()
					if ans is None:
						diff = datetime.now(timezone.utc) - item.tm_stmp
						seconds_passed = diff.total_seconds()
						seconds_limit = item.minutes_limit * 60
						if seconds_passed > seconds_limit : # If it has expired
							messages.error(request, 'Question has expired', extra_tags='alert-warning')  
							return redirect('student:student_codeinput')
						else:
							context = {
							'unit_code' : item.question.topic_id.unit_id.code,
							'unit_title' : item.question.topic_id.unit_id.title,
							'topic_num' : item.question.topic_id.number,
							'topic_title' : item.question.topic_id.name,
							'ans1' : item.question.ans_1,
							'ans2' : item.question.ans_2,
							'ans3' : item.question.ans_3,
							'ans4' : item.question.ans_4,
							'question_code' : code
							}
							request.session['question_data'] = context
							return redirect('student:student_answer')
					else:
						messages.error(request, 'Duplicate answer is not allowed for a question.', extra_tags='alert-warning')  
						return redirect('student:student_codeinput')
				else:
					messages.error(request, 'Not your class question code.', extra_tags='alert-warning')  
					return redirect('student:student_codeinput')
			else:
				messages.error(request, 'No matching question code.', extra_tags='alert-warning')  
				return redirect('student:student_codeinput')
	else:
		form = codeForm()
		user_dict['form'] = form
		return render(request, 'student/studentInput.html', user_dict)

@login_required
@is_student
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
			
			# Get the details of the question answered
			context = request.session.get('question_data')
			question_answered = Published_Question.objects.filter(code=context['question_code']).first()

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

			t_day = Teaching_Day.objects.filter(c_id=class_item, date_td=datetime.now(timezone.utc).date()).first()
			if t_day is None:
				return HttpResponse('Unexpected error')

			# Get IP address of student
			client_ip, is_routable = get_client_ip(request)
			
			if client_ip is None:
				client_ip = '0.0.0.0'
			
			# Create a new Answer object and save it to the database
			new_answer = Answer(s_id=std, q_id=question_answered, teach_day=t_day, ans=selection, ip_addr=client_ip)
			new_answer.save()
			
			request.session['question_data'] = None 
			
			return redirect('student:student_index')
	else:
		context1 = request.session.get('question_data')
		if context1 is not None:
			user = request.user
			context2 = get_std_context(user)
			user_dict = context1.copy()
			user_dict.update(context2)
			user_dict['unit_code'] = context1['unit_code']
			user_dict['topic_num'] = context1['topic_num']
			user_dict['topic_title'] = context1['topic_title']
			return render(request, 'student/studentQuestion.html', user_dict)
		else:
			messages.error(request, 'Input question code first.', extra_tags='alert-warning')  
			return redirect('student:student_codeinput')

@login_required
@is_student
def student_stats(request, unit_t, period_id):
	user = request.user
	period = "".join(period_id.split()).upper().replace(',','-')
	unit = Unit.objects.filter(code=unit_t).first()
	student = Student.objects.filter(user=user).first()
	period = Teaching_Period.objects.filter(id=period).first()
	
	user_dict = get_std_context(user)
	user_dict['graph'] = attendance_graph(unit, period, student)
	user_dict['s_unit_code'] = unit.code
	user_dict['s_period'] = period_id

	return render(request, 'student/studentStats.html', user_dict)

@login_required
@is_student
def student_error(request):
	user = request.user
	user_dict = get_std_context(user)
	return render(request, 'student/error.html', user_dict)

@login_required
@is_student
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
