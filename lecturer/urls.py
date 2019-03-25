from lecturer import views
from django.conf.urls import url
from django.urls import path

#TEMPLATE TAGGING
app_name = 'lecturer'

urlpatterns = [
	path('', views.lect_home, name='lect_home'),
	path('units/<str:unit_code>/', views.lect_units, name='lect_units'),
	url(r'^publish/sh=(?P<q_id>\d+)/$', views.lect_publish, name='lect_publish'),
	url('user_login', views.user_logout, name='user_logout'),
	url(r'^class/$', views.lect_class, name='lect_class')
]
