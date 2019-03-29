from django.db import models
from administrative.models import Course
from lecturer.models import Published_Question, Class, Teaching_Day
from django.contrib.auth.models import User

class Student(models.Model):

    """
        Django's Model to represent the student
		class in the MySQL Database.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', default='')
    s_class = models.ManyToManyField(Class)                 # Many Students to Many Classes
    s_course= models.ManyToManyField(Course)                # Many Students to Many Courses

class Answer(models.Model):

	"""
		Django's Model to represent the Asnwer
		class in the MySQL.
	"""

	s_id		= models.ForeignKey(Student, on_delete=models.PROTECT)		# Student ID
	q_id		= models.ForeignKey(Published_Question, on_delete=models.PROTECT)		# Question ID
	teach_day	= models.ForeignKey(Teaching_Day, on_delete=models.PROTECT)	# Teaching Day ID
	ans		= models.CharField(max_length=255)				# Answer Option
	tm_stmp		= models.DateTimeField()					# Time Stamp
	ip_addr		= models.CharField(max_length=15)				# IP Type
