from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):

	"""
		Django's Model to represent the course
		class in the MySQL Database.
	"""
	id	= models.CharField(primary_key=True, max_length=6)	# Course ID
	title	= models.CharField(max_length=30)			# Course's Title
	school	= models.CharField(max_length=30)			# School which owns the Course

class Unit(models.Model):

	"""
		Django's Model to represent the unit
		class in the MySQL database.
	"""

	code	= models.CharField(primary_key=True, max_length=6)	# Unit's code
	title 	= models.CharField(max_length=30)			# Unit Title
	credits = models.PositiveIntegerField()				# Unit's max credits

class Building(models.Model):

	"""
		Django's Model to represent the building
		class in the MySQL database.
	"""

	code	= models.CharField(primary_key=True, max_length=4)	# Building's Code
	name	= models.CharField(max_length=20)			# Building's Name

class Room(models.Model):

        """
                Django's Model to represent the room
                class in MySQL database.
        """

        id      = models.CharField(primary_key=True, max_length=10)     # Room's ID
        code    = models.PositiveIntegerField()                         # Room's Code
        bd_code = models.ForeignKey(Building, on_delete=models.PROTECT)  # Building Code
        level   = models.IntegerField()                                 # Room's level/Floor
        capacity= models.PositiveIntegerField()                         # Room's Capacity

class Teaching_Period(models.Model):

	"""
		Django's Model to represent the teaching period
		class in the MySQL database.
	"""

	id 	= models.CharField(primary_key=True, max_length=10)	# Teaching Period ID
	name	= models.CharField(max_length=20)			# Teaching Period Name
	st_date	= models.DateField()					# Starting Date
	en_date	= models.DateField()					# Ending Date

class Employee(models.Model):

	"""
		Django's Model to represent the staff
		class in the MySQL database.
	"""

	user 	= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', default='')
	dpt		= models.CharField(max_length=29, blank=True, default='')		# Department
	pstn	= models.CharField(max_length=19, blank=True, default='')		# Position

class Class(models.Model):

	"""
		Django's Model to represent the Class
		class in the MySQL database.
	"""

	id		= models.CharField(primary_key=True, max_length=9)		# Class ID - ICT302
	course_id	= models.ForeignKey(Course, on_delete=models.PROTECT)		# Course ID
	unit_id		= models.ForeignKey(Unit, on_delete=models.PROTECT)		# Unit ID
	t_period	= models.ForeignKey(Teaching_Period, on_delete=models.PROTECT)	# Teaching Period ID
	staff_id	= models.ForeignKey(Employee, on_delete=models.PROTECT, related_name='lecturer_id')		# Staff ID
	time_commi	= models.CharField(max_length=2)				# Time Commitment

class Question(models.Model):

	"""
		Django's Model to represent the Question
		class in the MySQL database.
	"""

	text	= models.TextField()					# Question
	ans_1	= models.TextField()					# Answer option 1
	ans_2	= models.TextField()					# Answer option 2
	ans_3	= models.TextField()					# Answer option 3
	ans_4	= models.TextField()					# Answer option 4
	unit_id	= models.ForeignKey(Unit, on_delete=models.PROTECT)	# Question's unit code
	staff_id= models.ForeignKey(Employee, on_delete=models.PROTECT)	# Question's Creator

class Student(models.Model):

        """
                Django's Model to represent the student
                class in the MySQL Database.
        """

        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile', default='')
        s_class = models.ManyToManyField(Class)                 # Many Students to Many Classes
        s_course= models.ManyToManyField(Course)                # Many Students to Many Courses

class Teaching_Day(models.Model):

        """
                Django's Model to represent the Teaching Day
                class in the MySQL database.
        """

        r_id    = models.ForeignKey(Room, on_delete=models.PROTECT)     # Room ID
        c_id    = models.ForeignKey(Class, on_delete=models.PROTECT)    # Class ID
        st_time = models.DateTimeField()                                # Starting Time
        en_time = models.DateTimeField()                                # Ending Time

class Answer(models.Model):

	"""
		Django's Model to represent the Asnwer
		class in the MySQL.
	"""

	s_id		= models.ForeignKey(Student, on_delete=models.PROTECT)		# Student ID
	q_id		= models.ForeignKey(Question, on_delete=models.PROTECT)		# Question ID
	teach_day	= models.ForeignKey(Teaching_Day, on_delete=models.PROTECT)	# Teaching Day ID
	ans		= models.CharField(max_length=50)				# Answer Option
	tm_stmp		= models.DateTimeField()					# Time Stamp
	ip_t		= models.CharField(max_length=8)				# IP Type
