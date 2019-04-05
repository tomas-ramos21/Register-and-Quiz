from administrative.models import Course, Unit, Room, Building, Teaching_Period, Employee, Topic
from lecturer.models import Class
from student.models import Student
from django.contrib.auth.models import User


e1 = Employee.objects.filter(user='20185512').first()

topic1 = Topic(number=1, name='SA part 1', unit_id='ICT373')
topic1.save()

topic2 = Topic(number=2, name='SA part 2', unit_id='ICT373')
topic1.save()

topic3 = Topic(number=3, name='167 part 1', unit_id='ICT167')
topic3.save()

topic4 = Topic(number=4, name='167 part 2', unit_id='ICT167')
topic4.save()

# Question for ICT373
qn1 = Question(title='SA question 1',text='What programming language?',ans_1='Java', ans2='Python', topic_id=topic1, staff_id=e1)
qn1.save()

qn1 = Question(title='SA question 2',text='What programming language?',ans_1='Java', ans2='Python', topic_id=topic1, staff_id=e1)
qn1.save()