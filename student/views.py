from django.shortcuts import render

def student_home(request):
	student_dict = {'name_header':'Rodney',
			'name_menu':'Rodney'}
	return render(request, 'student/student.html', student_dict)
