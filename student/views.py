from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from login.models import Student, Unit


app_name = 'student'

def index(request):
	return HttpResponseRedirect(reverse('student:student_dashboard'))

def student_dashboard(request):
	user = request.user
	std = Student.objects.get(user=user)

	enrolled_class = list(std.s_class.all())

	unit_id_list = [x.unit_id for x in enrolled_class]
	unit_name_list = [x.title for x in unit_id_list]

	context = {key:value for key, value in zip(unit_id_list, unit_name_list)}
	context['f_name'] = request.user.first_name
	context['l_name'] = request.user.first_name + ' ' + request.user.last_name


	return render(request, 'student/student.html', context)
