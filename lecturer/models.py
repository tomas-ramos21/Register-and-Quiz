from django.db import models
from administrative.models import Unit, Course, Teaching_Period, Room, Employee

class Question(models.Model):

    text = models.CharField(max_length=255)
    ans_1 = models.CharField(max_length=255)
    ans_2 = models.CharField(max_length=255)
    ans_3 = models.CharField(max_length=255)
    ans_4 = models.CharField(max_length=255)
    unit_id	= models.ForeignKey(Unit, on_delete=models.PROTECT)
    staff_id = models.ForeignKey(Employee, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('text', 'staff_id'),)


class Class(models.Model):
    """
        Django's Model to represent the Class
        class in the MySQL database.
    """
    id = models.CharField(primary_key=True, max_length=9)
    course_id = models.ForeignKey(Course, on_delete=models.PROTECT)
    unit_id	= models.ForeignKey(Unit, on_delete=models.PROTECT)
    t_period = models.ForeignKey(Teaching_Period, on_delete=models.PROTECT)
    staff_id = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='lecturer_id')
    time_commi = models.CharField(max_length=2)

class Teaching_Day(models.Model):
    """
        Django's Model to represent the Teaching Day
        class in the MySQL database.
    """
    r_id    = models.ForeignKey(Room, on_delete=models.PROTECT)     # Room ID
    c_id    = models.ForeignKey(Class, on_delete=models.PROTECT)    # Class ID
    st_time = models.DateTimeField()                                # Starting Time
    en_time = models.DateTimeField()                                # Ending Time

class Published_Question(models.Model):
	id = models.CharField(primary_key = True, max_length=30) #qhdewsk_10:30:00
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	code = models.CharField(max_length=20) #qhdewsk
	tm_stmp = models.DateTimeField() #10:30:00
	seconds_limit = models.PositiveIntegerField() #240
