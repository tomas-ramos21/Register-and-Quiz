from django.conf.urls import url
from student import views

app_name ='student'

urlpatterns = [
	url(r'^my/$', views.student_dashboard, name='student_dashboard'),	
]

