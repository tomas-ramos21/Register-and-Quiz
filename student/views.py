from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from lecturer.models import Published_Question
from administrative.models import Unit
from student.models import Student
from datetime import datetime, timedelta, timezone
from student.forms import codeForm

app_name = 'student'

def index(request):
	return HttpResponseRedirect(reverse('student:student_dashboard'))

def student_dashboard(request):
	user = request.user
	std = Student.objects.filter(user=user).first()

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
		enrolled_class = std.s_class.all()
		unit_list  = [x.unit_id for x in enrolled_class]
		t_period = [x.t_period for x in enrolled_class]
		context = {
		'f_name' : request.user.first_name,
		'l_name' : request.user.first_name + ' ' + request.user.last_name,
		'enrolled_class' : enrolled_class,
		'unit_list' : unit_list,
		't_period' : t_period,
		}
		return render(request, 'student/student_dashboard.html', context)
	else:
		return HttpResponse('Not registered as a student')



def student_codeinput(request):
	if request.method == 'POST':
		form = codeForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			code = cd.get('code')
			item = Published_Question.objects.filter(code=code).first()
			if item != None:
				diff = datetime.now(timezone.utc) - item.tm_stmp
				if diff > timedelta(item.seconds_limit):
					return HttpResponse('Question has expired.')
				else:
					context = {
					'unit_code' : item.question.unit_id.code,
					'unit_title' : item.question.unit_id.title,
					'ans1' : item.question.ans_1,
					'ans2' : item.question.ans_2,
					'ans3' : item.question.ans_3,
					'ans4' : item.question.ans_4,
					}
					request.session['question_data'] = context
					return student_question(request)
			else:
				return HttpResponse('No matching question code.')
	else:
		form = codeForm()

	return render(request, 'student/studentInput.html', {'form':form})

def student_question(request):
	context = request.session.get('question_data')
	return render(request, 'student/studentQuestion.html', context)
