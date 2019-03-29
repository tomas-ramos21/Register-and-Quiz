from django.conf.urls import url
from student import views
from django.urls import path

app_name ='student'

urlpatterns = [
	path('', views.student_index, name='student_index'),
	path('my/', views.student_dashboard, name='student_dashboard'),	
	path('code-input/', views.student_codeinput, name='student_codeinput'),
	path('submit-answer/', views.student_answer, name='student_answer'),
	path('user_logout', views.user_logout, name='user_logout'),
]

