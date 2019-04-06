from administrative.models import Course, Unit, Room, Building, Teaching_Period, Employee
from lecturer.models import Class, Topic, Question, Published_Question, Teaching_Day
from student.models import Student, Answer
from django.contrib.auth.models import User
from datetime import datetime, timezone

user = User.objects.filter(username='20185512').first()
e1 = Employee.objects.filter(user=user).first()

u1 = Unit.objects.filter(code='ICT373').first()
u2 = Unit.objects.filter(code='ICT167').first()

# Topic for ICT373
topic1 = Topic(number=1, name='SA part 1', unit_id=u1)
topic1.save()

topic2 = Topic(number=2, name='SA part 2', unit_id=u1)
topic1.save()

# Topic for ICT167
topic3 = Topic(number=3, name='167 part 1', unit_id=u2)
topic3.save()

topic4 = Topic(number=4, name='167 part 2', unit_id=u2)
topic4.save()

# Question for ICT373
qn1 = Question(title='SA question 1',text='What programming language?',ans_1='Java', ans_2='Python', topic_id=topic1, staff_id=e1)
qn1.save()

qn2 = Question(title='SA question 2',text='Arrays start at...?',ans_1='0', ans_2='1', topic_id=topic1, staff_id=e1)
qn2.save()

qn3 = Question(title='SA question 3',text='What is software?',ans_1='application', ans_2='program', topic_id=topic1, staff_id=e1)
qn3.save()

# for day 2
qn4 = Question(title='SA question 4',text='What is architecture?',ans_1='framework', ans_2='blueprint', topic_id=topic1, staff_id=e1)
qn4.save()

qn5 = Question(title='SA question 5',text='What is algorithm',ans_1='0', ans_2='1', topic_id=topic1, staff_id=e1)
qn5.save()

qn6 = Question(title='SA question 6',text='What is data structure?',ans_1='application', ans_2='program', topic_id=topic1, staff_id=e1)
qn6.save()

# Question for ICT167
qn7 = Question(title='PCP question 1',text='What programming language?',ans_1='Java', ans_2='Python', topic_id=topic3, staff_id=e1)
qn7.save()

qn8 = Question(title='PCP question 2',text='Arrays start at...?',ans_1='0', ans_2='1', topic_id=topic3, staff_id=e1)
qn8.save()

qn9 = Question(title='PCP question 3',text='What is software?',ans_1='application', ans_2='program', topic_id=topic3, staff_id=e1)
qn9.save()

qn10 = Question(title='PCP question 4',text='What is architecture?',ans_1='framework', ans_2='blueprint', topic_id=topic4, staff_id=e1)
qn10.save()

qn11 = Question(title='PCP question 5',text='What is algorithm',ans_1='0', ans_2='1', topic_id=topic4, staff_id=e1)
qn11.save()

tp = Teaching_Period.objects.filter(id='TJA-2019').first()

class1=Class(unit_id=u1,t_period=tp,staff_id=e1,time_commi='ft',code='A') #ICT373
class1.save()

class2=Class(unit_id=u2,t_period=tp,staff_id=e1,time_commi='ft',code='A') #ICT167
class2.save()

#2019-3-31
dt = datetime(year=2019, month=3, day=31, hour=10, minute=0, tzinfo=timezone.utc)
dt1 = datetime(year=2019, month=3, day=31, hour=10, minute=15, tzinfo=timezone.utc)
dt2 = datetime(year=2019, month=3, day=31, hour=11, minute=0, tzinfo=timezone.utc)
dt3 = datetime(year=2019, month=3, day=31, hour=15, minute=10, tzinfo=timezone.utc)
dt4 = datetime(year=2019, month=3, day=31, hour=15, minute=30, tzinfo=timezone.utc)

# 2019-4-10
dt5 = datetime(year=2019, month=4, day=10, hour=14, minute=0, tzinfo=timezone.utc)
dt6 = datetime(year=2019, month=4, day=10, hour=15, minute=0, tzinfo=timezone.utc)
dt7 = datetime(year=2019, month=4, day=10, hour=15, minute=30, tzinfo=timezone.utc)
dt8 = datetime(year=2019, month=4, day=10, hour=18, minute=0, tzinfo=timezone.utc)
dt9 = datetime(year=2019, month=4, day=10, hour=18, minute=30, tzinfo=timezone.utc)
dt10 = datetime(year=2019, month=4, day=10, hour=19, minute=0, tzinfo=timezone.utc)

user1 = User.objects.filter(username='33317512').first()
std1 = Student.objects.filter(user=user1).first()
user2 = User.objects.filter(username='33317513').first()
std2 = Student.objects.filter(user=user2).first()

user3 = User.objects.filter(username='33317514').first()
std3 = Student.objects.filter(user=user3).first()
user4 = User.objects.filter(username='33317515').first()
std4 = Student.objects.filter(user=user4).first()
user5 = User.objects.filter(username='33317516').first()
std5 = Student.objects.filter(user=user5).first()
user6 = User.objects.filter(username='33317517').first()
std6 = Student.objects.filter(user=user6).first()
user7 = User.objects.filter(username='33317518').first()
std7 = Student.objects.filter(user=user7).first()
user8 = User.objects.filter(username='33317519').first()
std8 = Student.objects.filter(user=user8).first()
user9 = User.objects.filter(username='33317520').first()
std9 = Student.objects.filter(user=user9).first()
user10 = User.objects.filter(username='33317521').first()
std10 = Student.objects.filter(user=user10).first()

room = Room.objects.filter(id='WE302').first()
room2 = Room.objects.filter(id='WE510').first()

# for ICT373
tp1 = Teaching_Day(r_id=room, c_id=class1, date_td=dt1.date())
tp1.save()
tp2 = Teaching_Day(r_id=room, c_id=class2, date_td=dt1.date())
tp2.save()
# for
tp3 = Teaching_Day(r_id=room2, c_id=class1, date_td=dt5.date())
tp3.save()
tp4 = Teaching_Day(r_id=room2, c_id=class2, date_td=dt5.date())
tp4.save()

# Question fot ICT373 - 2019-3-31
qn1_p = Published_Question(code=1, question=qn1, q_class=class1, tm_stmp=dt1, minutes_limit=1)
qn1_p.save() #3

ans1_1 = Answer(s_id=std1, q_id=qn1_p, teach_day=tp1,ans='Java',tm_stmp=dt1,ip_addr='0.0.0.0')
ans1_1.save()
ans1_2 = Answer(s_id=std2, q_id=qn1_p, teach_day=tp1,ans='Python',tm_stmp=dt1,ip_addr='0.0.0.0')
ans1_2.save()
ans1_3 = Answer(s_id=std3, q_id=qn1_p, teach_day=tp1,ans='Java',tm_stmp=dt1,ip_addr='0.0.0.0')
ans1_3.save()

qn2_p = Published_Question(code=2, question=qn2, q_class=class1, tm_stmp=dt2, minutes_limit=1)
qn2_p.save() #5

ans2_1 = Answer(s_id=std4, q_id=qn2_p, teach_day=tp1,ans='0',tm_stmp=dt1,ip_addr='0.0.0.0')
ans2_1.save()
ans2_2 = Answer(s_id=std5, q_id=qn2_p, teach_day=tp1,ans='1',tm_stmp=dt1,ip_addr='0.0.0.0')
ans2_2.save()
ans2_3 = Answer(s_id=std6, q_id=qn2_p, teach_day=tp1,ans='0',tm_stmp=dt1,ip_addr='0.0.0.0')
ans2_3.save()
ans2_4 = Answer(s_id=std1, q_id=qn2_p, teach_day=tp1,ans='1',tm_stmp=dt1,ip_addr='0.0.0.0')
ans2_4.save()
ans2_5 = Answer(s_id=std2, q_id=qn2_p, teach_day=tp1,ans='1',tm_stmp=dt1,ip_addr='0.0.0.0')
ans2_5.save()

qn3_p = Published_Question(code=3, question=qn3, q_class=class1, tm_stmp=dt3, minutes_limit=1)
qn3_p.save() #10

ans3_1 = Answer(s_id=std1, q_id=qn3_p, teach_day=tp1,ans='application',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_1.save()
ans3_2 = Answer(s_id=std2, q_id=qn3_p, teach_day=tp1,ans='program',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_2.save()
ans3_3 = Answer(s_id=std3, q_id=qn3_p, teach_day=tp1,ans='program',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_3.save()
ans3_4 = Answer(s_id=std4, q_id=qn3_p, teach_day=tp1,ans='application',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_4.save()
ans3_5 = Answer(s_id=std5, q_id=qn3_p, teach_day=tp1,ans='program',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_5.save()
ans3_6 = Answer(s_id=std6, q_id=qn3_p, teach_day=tp1,ans='program',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_6.save()
ans3_7 = Answer(s_id=std7, q_id=qn3_p, teach_day=tp1,ans='application',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_7.save()
ans3_8 = Answer(s_id=std8, q_id=qn3_p, teach_day=tp1,ans='application',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_8.save()
ans3_9 = Answer(s_id=std9, q_id=qn3_p, teach_day=tp1,ans='program',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_9.save()
ans3_10 = Answer(s_id=std10, q_id=qn3_p, teach_day=tp1,ans='application',tm_stmp=dt1,ip_addr='0.0.0.0')
ans3_10.save()

# ICT373 2019-4-10
qn4_p = Published_Question(code=4, question=qn4, q_class=class1, tm_stmp=dt5, minutes_limit=1)
qn4_p.save() #10

ans4_1 = Answer(s_id=std1, q_id=qn4_p, teach_day=tp3,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_1.save()
ans4_2 = Answer(s_id=std2, q_id=qn4_p, teach_day=tp3,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_2.save()
ans4_3 = Answer(s_id=std3, q_id=qn4_p, teach_day=tp3,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_3.save()
ans4_4 = Answer(s_id=std4, q_id=qn4_p, teach_day=tp3,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_4.save()
ans4_5 = Answer(s_id=std5, q_id=qn4_p, teach_day=tp3,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_5.save()
ans4_6 = Answer(s_id=std6, q_id=qn4_p, teach_day=tp3,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_6.save()
ans4_7 = Answer(s_id=std7, q_id=qn4_p, teach_day=tp3,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_7.save()
ans4_8 = Answer(s_id=std8, q_id=qn4_p, teach_day=tp3,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_8.save()
ans4_9 = Answer(s_id=std9, q_id=qn4_p, teach_day=tp3,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_9.save()
ans4_10 = Answer(s_id=std10, q_id=qn4_p, teach_day=tp3,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans4_10.save()

qn5_p = Published_Question(code=5, question=qn5, q_class=class1, tm_stmp=dt6, minutes_limit=1)
qn5_p.save() #5
ans5_5 = Answer(s_id=std5, q_id=qn5_p, teach_day=tp3,ans='0',tm_stmp=dt5,ip_addr='0.0.0.0')
ans5_5.save()
ans5_6 = Answer(s_id=std6, q_id=qn5_p, teach_day=tp3,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans5_6.save()
ans5_7 = Answer(s_id=std7, q_id=qn5_p, teach_day=tp3,ans='0',tm_stmp=dt5,ip_addr='0.0.0.0')
ans5_7.save()
ans5_8 = Answer(s_id=std8, q_id=qn5_p, teach_day=tp3,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans5_8.save()
ans5_9 = Answer(s_id=std9, q_id=qn5_p, teach_day=tp3,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans5_9.save()

qn6_p = Published_Question(code=6, question=qn6, q_class=class1, tm_stmp=dt7, minutes_limit=1)
qn6_p.save() #7
ans6_1 = Answer(s_id=std5, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_1.save()
ans6_2 = Answer(s_id=std6, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_2.save()
ans6_3 = Answer(s_id=std7, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_3.save()
ans6_4 = Answer(s_id=std8, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_4.save()
ans6_5 = Answer(s_id=std9, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_5.save()
ans6_6 = Answer(s_id=std1, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_6.save()
ans6_7 = Answer(s_id=std2, q_id=qn6_p, teach_day=tp3,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans6_7.save()

# Question fot ICT167 - 2019-3-31
qn7_p = Published_Question(code=7, question=qn7, q_class=class2, tm_stmp=dt3, minutes_limit=1)
qn7_p.save() #2

ans7_1 = Answer(s_id=std8, q_id=qn7_p, teach_day=tp2,ans='Java',tm_stmp=dt5,ip_addr='0.0.0.0')
ans7_1.save()
ans7_2 = Answer(s_id=std9, q_id=qn7_p, teach_day=tp2,ans='Java',tm_stmp=dt5,ip_addr='0.0.0.0')
ans7_2.save()

qn8_p = Published_Question(code=8, question=qn8, q_class=class2, tm_stmp=dt4, minutes_limit=1)
qn8_p.save() #5

ans8_1 = Answer(s_id=std8, q_id=qn8_p, teach_day=tp2,ans='0',tm_stmp=dt5,ip_addr='0.0.0.0')
ans8_1.save()
ans8_2 = Answer(s_id=std9, q_id=qn8_p, teach_day=tp2,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans8_2.save()

# Question fot ICT373 - 2019-4-10
qn9_p = Published_Question(code=9, question=qn9, q_class=class2, tm_stmp=dt8, minutes_limit=1)
qn9_p.save() #10

ans9_1 = Answer(s_id=std1, q_id=qn9_p, teach_day=tp4,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_1.save()
ans9_2 = Answer(s_id=std2, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_2.save()
ans9_3 = Answer(s_id=std3, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_3.save()
ans9_4 = Answer(s_id=std4, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_4.save()
ans9_5 = Answer(s_id=std5, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_5.save()
ans9_6 = Answer(s_id=std6, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_6.save()
ans9_7 = Answer(s_id=std7, q_id=qn9_p, teach_day=tp4,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_7.save()
ans9_8 = Answer(s_id=std8, q_id=qn9_p, teach_day=tp4,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_8.save()
ans9_9 = Answer(s_id=std9, q_id=qn9_p, teach_day=tp4,ans='application',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_9.save()
ans9_10 = Answer(s_id=std10, q_id=qn9_p, teach_day=tp4,ans='program',tm_stmp=dt5,ip_addr='0.0.0.0')
ans9_10.save()

qn10_p = Published_Question(code=10, question=qn10, q_class=class2, tm_stmp=dt9, minutes_limit=1)
qn10_p.save() #10

ans10_1 = Answer(s_id=std1, q_id=qn10_p, teach_day=tp4,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_1.save()
ans10_2 = Answer(s_id=std2, q_id=qn10_p, teach_day=tp4,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_2.save()
ans10_3 = Answer(s_id=std3, q_id=qn10_p, teach_day=tp4,ans='framework',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_2.save()
ans10_4 = Answer(s_id=std4, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_4.save()
ans10_5 = Answer(s_id=std5, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_5.save()
ans10_6 = Answer(s_id=std6, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_6.save()
ans10_7 = Answer(s_id=std7, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_7.save()
ans10_8 = Answer(s_id=std8, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_8.save()
ans10_9 = Answer(s_id=std9, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_9.save()
ans10_10 = Answer(s_id=std10, q_id=qn10_p, teach_day=tp4,ans='blueprint',tm_stmp=dt5,ip_addr='0.0.0.0')
ans10_10.save()

qn11_p = Published_Question(code=11, question=qn11, q_class=class2, tm_stmp=dt10, minutes_limit=1)
qn11_p.save() #7

ans11_1 = Answer(s_id=std1, q_id=qn11_p, teach_day=tp4,ans='0',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_1.save()
ans11_2 = Answer(s_id=std2, q_id=qn11_p, teach_day=tp4,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_2.save()
ans11_3 = Answer(s_id=std3, q_id=qn11_p, teach_day=tp4,ans='0',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_3.save()
ans11_4 = Answer(s_id=std4, q_id=qn11_p, teach_day=tp4,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_4.save()
ans11_5 = Answer(s_id=std5, q_id=qn11_p, teach_day=tp4,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_5.save()
ans11_6 = Answer(s_id=std6, q_id=qn11_p, teach_day=tp4,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_6.save()
ans11_7 = Answer(s_id=std7, q_id=qn11_p, teach_day=tp4,ans='1',tm_stmp=dt5,ip_addr='0.0.0.0')
ans11_7.save()