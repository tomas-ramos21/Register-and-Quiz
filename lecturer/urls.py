from lecturer import views
from django.conf.urls import url

#TEMPLATE TAGGING
app_name = 'lecturer'


urlpatterns = [
	url(r'^lecturer/$', views.lect_home, name='lect_home'),
	url('user_login', views.user_logout, name='user_logout'),
]
