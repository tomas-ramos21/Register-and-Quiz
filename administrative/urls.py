from django.conf.urls import url
from administrative import views
from generic import utils

# TEMPLATE TAGGING
app_name = 'administrative'

urlpatterns = [
	url(r'^administrative/$', views.admin_home, name='admin_home'),
	url(r'^accountM/$', views.acc_management, name='acc_management'),
	url(r'^unitsM/$', views.unit_management, name='unit_management'),
	url(r'^teachingspace/$', views.space_management, name='space_management'),
	url(r'^lectAccAdd.html/$', views.lecturer_creation, name='lecturer_creation'),
	url(r'^stuAccAdd.html/$', views.student_creation, name='student_creation'),
	url('user_login', views.user_logout, name='user_logout'),
]
