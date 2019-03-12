from django.shortcuts import render

def lect_home(request):
	lect_dict = {'name_header':'Rodney',
		     'name_menu':'Rodney'}
	return render(request, "Lecturer/Lecturer.html", lect_dict)
