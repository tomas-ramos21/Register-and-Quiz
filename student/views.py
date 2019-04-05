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
from generic.utils import get_std_context, is_expired
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
						if is_expired(item):
							messages.error(request, 'Question has expired', extra_tags='alert-warning')
							return redirect('student:student_codeinput')
						else:
							request.session['question_data'] = item.code
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

			# Get the student object who submitted the answer
			user = request.user
			std = Student.objects.filter(user=user).first()
			
			# Get the details of the question answered
			context = request.session.get('question_data')
			if context is not None:
				question_answered = Published_Question.objects.filter(code=context).first()
				if question_answered is not None:
					if is_expired(question_answered):
						messages.error(request, 'Question has expired', extra_tags='alert-warning')
						return redirect('student:student_codeinput')
					else:
						selection = request.POST.get('choice')

						class_item = question_answered.q_class

						enrolled_class = std.s_class.all()

						if class_item in enrolled_class:
							t_day = Teaching_Day.objects.filter(c_id=class_item, date_td=datetime.now(timezone.utc).date()).first()

							if t_day is None:
								messages.error(request, 'No matching Teaching Day found.', extra_tags='alert-warning')
								return redirect('student:student_codeinput')

							# Get IP address of student
							client_ip, is_routable = get_client_ip(request)

							if client_ip is None:
								client_ip = '0.0.0.0'

							# Create a new Answer object and save it to the database
							ans = Answer.objects.filter(s_id=std, q_id=question_answered)
							if ans.exists() == False :
								new_answer = Answer(s_id=std, q_id=question_answered, teach_day=t_day, ans=selection, ip_addr=client_ip)
								new_answer.save()

							request.session['question_data'] = None

							messages.success(request, 'Successfully submitted answer on Question: ' + question_answered.question.title, extra_tags='alert-success')
							return redirect('student:student_codeinput')
						else:
							messages.error(request, 'Not your class question.', extra_tags='alert-warning')
							return redirect('student:student_codeinput')
	else:
		context = request.session.get('question_data')
		if context is not None:
			user = request.user
			user_context = get_std_context(user)
			item = Published_Question.objects.filter(code=context).first()
			if item is not None:
				if is_expired(item):
					messages.error(request, 'Question has expired', extra_tags='alert-warning')
					return redirect('student:student_codeinput')
				else:
					context = {
						'unit_code' : item.question.topic_id.unit_id.code,
						'unit_title' : item.question.topic_id.unit_id.title,
						't_num' : item.question.topic_id.number,
						't_name' : item.question.topic_id.name,
						'q_title' : item.question.title,
						'ans1' : item.question.ans_1,
						'ans2' : item.question.ans_2,
					 	'ans3' : item.question.ans_3,
						'ans4' : item.question.ans_4,
					}
					user_dict = user_context.copy()
					user_dict.update(context)
					return render(request, 'student/studentQuestion.html', user_dict)
			else:
				return redirect('student:student_codeinput')
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
