from django.conf.urls import url
from django.urls import path
from administrative import views
from generic import utils

# TEMPLATE TAGGING
app_name = 'administrative'

urlpatterns = [
	path('my/', views.admin_home, name='admin_home'),
	url(r'^account-management/$', views.acc_management, name='acc_management'),
	url(r'^unit-management/$', views.unit_management, name='unit_management'),
	url(r'^teaching-space-management/$', views.space_management, name='space_management'),
	url(r'^create-lecturer/$', views.employee_creation, name='employee_creation'),
	url(r'^create-student/$', views.student_creation, name='student_creation'),
	url(r'^stats/$', views.admin_stats, name='admin_stats'),
	url(r'^space_stats/$', views.space_stats, name='space_stats'),
	url(r'^attendance_stats/$', views.attendance_stats, name='attendance_stats'),
	url(r'^user-view/$', views.user_view, name='user_view'),
	url('user_login', views.user_logout, name='user_logout'),
]
