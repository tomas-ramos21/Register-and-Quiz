from django.db import models
import datetime
from administrative.models import Unit, Course, Teaching_Period, Room, Employee
from datetime import datetime

def today_utc():
    return datetime.utcnow().date()
	
class Topic(models.Model):

    id = models.AutoField(primary_key=True)
    number = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    unit_id = models.ForeignKey(Unit, on_delete=models.PROTECT)

class Question(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    ans_1 = models.CharField(max_length=255)
    ans_2 = models.CharField(max_length=255)
    ans_3 = models.CharField(max_length=255, null=True, blank=True)
    ans_4 = models.CharField(max_length=255, null=True, blank=True)
    topic_id = models.ForeignKey(Topic, on_delete=models.PROTECT)
    staff_id = models.ForeignKey(Employee, on_delete=models.PROTECT)

class Class(models.Model):
    """
        Django's Model to represent the Class
        class in the MySQL database.
    """
    time_commitments = (
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
    )
    id = models.AutoField(primary_key=True)
    unit_id	= models.ForeignKey(Unit, on_delete=models.PROTECT)
    t_period = models.ForeignKey(Teaching_Period, on_delete=models.PROTECT)
    staff_id = models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='lecturer_id')
    time_commi = models.CharField(max_length=2, choices=time_commitments)
    code = models.CharField(max_length=1)

class Teaching_Day(models.Model):
    """
        Django's Model to represent the Teaching Day
        class in the MySQL database.
    """

    id      = models.AutoField(primary_key=True)
    r_id    = models.ForeignKey(Room, on_delete=models.PROTECT)     # Room ID
    c_id    = models.ForeignKey(Class, on_delete=models.PROTECT)    # Class ID
    date_td = models.DateField(default=today_utc)

class Published_Question(models.Model):
    code = models.PositiveIntegerField(primary_key=True)               # Code - 123-456-789
    question = models.ForeignKey(Question, on_delete=models.PROTECT)   # Question object
    q_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    tm_stmp = models.DateTimeField(editable=False)                  # Time automatically added
    minutes_limit = models.PositiveIntegerField()                      # Time in seconds to answer
	
    def save(self, *args, **kwargs):
        if not self.tm_stmp:
            self.tm_stmp = datetime.utcnow()
        return super(Published_Question, self).save(*args, **kwargs)