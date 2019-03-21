from django.shortcuts import render
from login.views import login_required

app_name = 'student'

def student_dashboard(request, curr_user):
	student_dict = {
	'name_header': curr_user.first_name, 
	'name_menu' : curr_user.first_name + ' ' + curr_user.last_name 
	}
	return render(request, 'student/student.html', student_dict)
