from lecturer import views
from django.conf.urls import url
from django.urls import path

#TEMPLATE TAGGING
app_name = 'lecturer'

urlpatterns = [
	path('', views.lect_home, name='lect_home'),
	path('units/<str:unit_code>/', views.lect_units, name='lect_units'),
	path('publish/<int:q_id>/<int:topic_id>/<str:period_id>/', views.lect_publish, name='lect_publish'),
	url('user_login', views.user_logout, name='user_logout'),
	url(r'^class/$', views.lect_class, name='lect_class'),
	path('qstats/<str:published_id>', views.lect_q_stats, name='lect_q_stats'),
	url(r'^project/$', views.lect_project, name='lect_project'),
	path('error/', views.lect_error, name='lect_error'),
]
