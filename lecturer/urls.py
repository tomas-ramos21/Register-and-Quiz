from lecturer import views
from django.conf.urls import url

#TEMPLATE TAGGING
app_name = 'lecturer'


urlpatterns = [
	url(r'^lecturer/$', views.lect_home, name='lect_home'),
	url(r'^units/$', views.lect_units, name='lect_units'),
	url(r'^publish/$', views.lect_publish, name='lect_publish'),
	url('user_login', views.user_logout, name='user_logout'),
]
