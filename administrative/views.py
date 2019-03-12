from django.shortcuts import render

def admin_home(request):
	admin_dict = {'name_header':'Rodney',
		      'name_menu': 'Rodney'}
	return render(request, 'administrative/admin_home.html', admin_dict)

def acc_management(request):
	acc_dict = {'name_header':'Rodney',
		    'name_menu':'Rodney'}
	return render(request, 'administrative/accountM.html', acc_dict)

def unit_management(request):
	unit_dict = {'name_header':'Rodney',
		     'name_menu':'Rodney'}
	return render(request, 'administrative/unitsM.html', unit_dict)

def space_management(request):
	space_dict = {'name_header':'Rodney',
		      'name_menu':'Rodney'}
	return render(request, 'administrative/teachingspace.html', space_dict)
