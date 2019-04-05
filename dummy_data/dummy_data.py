from administrative.models import Course, Unit, Room, Building, Teaching_Period, Employee
from lecturer.models import Class
from student.models import Student
from django.contrib.auth.models import User

course1 = Course(id='CS', title='Computer Science', school='School of Engineering')
course1.save()

tp = Teaching_Period(id='TJA-2019', name='Trimester January', st_date='2019-1-1', en_date='2019-5-5')
tp.save()

building1 = Building(code='WE', name='Wilkie Edge')
building1.save()

room = Room(id='WE302', bd_code=building1, level=3, capacity=20)
room.save()

room2 = Room(id='WE510', bd_code=building1, level=5, capacity=30)
room2.save()

un1 = Unit(code='ICT373', title='Software Architecture', credits=3)
un1.save()
un1.course_id.add(course1)
un1.save()

un2 = Unit(code='ICT167', title='Principles of Computer Science', credits=3)
un2.save()
un2.course_id.add(course1)
un2.save()

u1 = User.objects.create_user(username='33317512', first_name='Madyarini Grace', last_name='Ariel', password='toortoor')
u1.save()
std1 = Student(user=u1)
std1.save()
std1.s_course.add(course1)
std1.save()

u2 = User.objects.create_user(username='33317513', first_name='Rodney Sim', last_name='Qui Young', password='toortoor')
u2.save()
std2 = Student(user=u2)
std2.save()
std2.s_course.add(course1)
std2.save()


u3 = User.objects.create_user(username='33317514', first_name='Tomas Aleixo', last_name='Ramos', password='toortoor')
u3.save()
std3 = Student(user=u3)
std3.save()
std3.s_course.add(course1)
std3.save()

u4 = User.objects.create_user(username='33317515', first_name='Kimberly Kim', last_name='Park', password='toortoor')
u4.save()
std4 = Student(user=u4)
std4.save()
std4.s_course.add(course1)
std4.save()

u5 = User.objects.create_user(username='33317516', first_name='Hien Ngoc', last_name='Chung', password='toortoor')
u5.save()
std5 = Student(user=u5)
std5.save()
std5.s_course.add(course1)
std5.save()

u6 = User.objects.create_user(username='33317517', first_name='Callista', last_name='Lavina', password='toortoor')
u6.save()
std6 = Student(user=u6)
std6.save()
std6.s_course.add(course1)
std6.save()

u7 = User.objects.create_user(username='33317518', first_name='Jonathan Williams', last_name='Wong', password='toortoor')
u7.save()
std7 = Student(user=u7)
std7.save()
std7.s_course.add(course1)
std7.save()

u8 = User.objects.create_user(username='33317519', first_name='Alevia', last_name='', password='toortoor')
u8.save()
std8 = Student(user=u8)
std8.save()
std8.s_course.add(course1)
std8.save()

u9 = User.objects.create_user(username='33317520', first_name='Caylisee', last_name='Queen', password='toortoor')
u9.save()
std9 = Student(user=u9)
std9.save()
std9.s_course.add(course1)
std9.save()

u10 = User.objects.create_user(username='33317521', first_name='Nanov', last_name='Dimitri', password='toortoor')
u10.save()
std1 = Student(user=u10)
std1.save()
std1.s_course.add(course1)
std1.save()

u13 = User.objects.create_user(username='20192200', first_name='Shri Rai', last_name='Singh', password='toortoor')
u13.save()
e13 = Employee(user=u13, dpt='Academic', pstn='Coordinator')
e13.save()
e13.units.add(un1)
e13.save()
e13.units.add(un2)
e13.save()

u11 = User.objects.create_user(username='201420S3', first_name='John Adams', last_name='Smith', password='toortoor')
u11.save()
e11 = Employee(user=u11, dpt='Finance', pstn='Staff')
e11.save()

u12 = User.objects.create_user(username='20185512', first_name='Chong Siew', last_name='Cheong', password='toortoor')
u12.save()
e12 = Employee(user=u12, dpt='Academic', pstn='Lecturer')
e12.save()
e12.units.add(un1)
e12.save()
e12.units.add(un2)
e12.save()

