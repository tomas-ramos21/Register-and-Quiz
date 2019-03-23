from django.conf.urls import url
from student import views
from django.urls import path

app_name ='student'

urlpatterns = [
	path('', views.index, name='student_index'),
	path('my/', views.student_dashboard, name='student_dashboard'),	
	path('code-input/', views.student_codeinput, name='student_codeinput'),
	path('question/', views.student_question, name='student_question'),
]

