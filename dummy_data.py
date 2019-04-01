python manage.py shell

from student.models import Student
from administrative.models import Administrative, Building, Room, Teaching_Period

building1 = Building(code='PM', name='PoMo')
building1.save()

room1 = Room(id='PM201', bd_code=building1, level=2, capacity=30)
room1.save()

u1 = User.objects.create_user(username='33317511', first_name='Ali Smith', last_name='Williams', password='student1')
u1.save()

