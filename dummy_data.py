from student.models import Student
from administrative.models import Course, Unit
from django.contrib.auth.models import User

course1 = Course(id='BIS', title='Business Information Systems', school='School of Engineering and Information Technology')
	
course1.save()
	
user = User.objects.create_user(username='33317510', first_name='Rodney Sim', last_name='Qui Young', password='toor')
user.save()
student = Student(user=user)
student.save()
student.s_course.add(course1)
student.save()