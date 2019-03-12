from django.conf.urls import url
from student import views

urlpatterns = [
	url(r'^$', views.student_home, name='student_home'),	
]
