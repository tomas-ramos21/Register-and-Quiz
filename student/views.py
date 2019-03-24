# Author: Madyarini Grace Ariel
# Date: 23-03-2019
# Purpose: Render HTML pages for both static and dynamic types.
# Last Modified By: Madyarini Grace Ariel
# Last Modified Date: 23-03-2019

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
<<<<<<< HEAD
from login.models import Student, Unit, Class, Teaching_Day, Published_Question, Answer
=======
from django.shortcuts import redirect
from lecturer.models import Published_Question
from administrative.models import Unit
from student.models import Student
>>>>>>> 09ec180253fc02967a9aa4516ed03cb70b930743
from datetime import datetime, timedelta, timezone
from student.forms import codeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ipware import get_client_ip

app_name = 'student'

@login_required
def index(request):
	"""
		Redirects to student's dashboard page.

		Parameters
		----------
		request: HTTP request object.
			Contains the request type sent by the user.
	"""
	return HttpResponseRedirect(reverse('student:student_dashboard'))

<<<<<<< HEAD
@login_required
=======
>>>>>>> 09ec180253fc02967a9aa4516ed03cb70b930743
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
<<<<<<< HEAD
	
	if std is not None:
=======

	if std != None:
		"""
		enrolled_class = list(std.s_class.all())

		unit_id_list = [x.unit_id for x in enrolled_class]
		unit_name_list = [x.title for x in unit_id_list]

		context = {key:value for key, value in zip(unit_id_list, unit_name_list)}
		context['f_name'] = request.user.first_name
		context['l_name'] = request.user.first_name + ' ' + request.user.last_name

		return render(request, 'student/student_dashboard.html', context)
		"""
>>>>>>> 09ec180253fc02967a9aa4516ed03cb70b930743
		enrolled_class = std.s_class.all()
		unit_list  = [x.unit_id for x in enrolled_class]
		t_period = [x.t_period for x in enrolled_class]
		context = {
		'f_name' : user.first_name,
		'fl_name' : user.first_name + ' ' + user.last_name,
		'enrolled_class' : enrolled_class,
		'unit_list' : unit_list,
		't_period' : t_period,
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
				if seconds_passed > item.seconds_limit:
					return HttpResponse('Question has expired.')
				else:
					context = {
					'unit_code' : item.question.unit_id.code,
					'unit_title' : item.question.unit_id.title,
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

<<<<<<< HEAD
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
			
			# Get the details of the question answered
			context = request.session.get('question_data')
			question_answered = Published_Question.objects.filter(code=context['question_code']).first().question
			
			# Get the details of the Teaching Day when the question was answered
			t_period = ''
			lecturer_first_name = ''
			
			enrolled_class = std.s_class.all()
			for x in enrolled_class:
				if x.unit_id == context['unit_code']:
					t_period = x.t_period
					lecturer_first_name = x.staff_id.user.first_name
					break
			
			class_id = context['unit_code'] + '_' + t_period + '_' + lecturer_first_name
			class_item = Class.objects.filter(id=class_id).first()
			t_day = Teaching_Day.objects.get(c_id=class_item, date_td=datetime.today())
			
			
			
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
			#new_answer = Answer(s_id=std, q_id=question_answered, teach_day=,ans=selection, tm_stmp=datetime.now(timezone.utc)
			
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
=======
def student_question(request):
	context = request.session.get('question_data')
	return render(request, 'student/studentQuestion.html', context)
>>>>>>> 09ec180253fc02967a9aa4516ed03cb70b930743
