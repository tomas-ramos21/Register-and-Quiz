from django.shortcuts import render
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

def lect_home(request):
	lect_dict = {'name_header':'Rodney',
		     'name_menu':'Rodney'}
	return render(request, "Lecturer/Lecturer.html", lect_dict)

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
    return HttpResponseRedirect(reverse('administrative:user_logout'))
