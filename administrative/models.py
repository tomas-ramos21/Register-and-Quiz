from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):

	"""
		Django's Model to represent the staff
		class in the MySQL database.
	"""

	user 	= models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile', default='')
	dpt		= models.CharField(max_length=255, blank=True, default='')		# Department
	pstn	= models.CharField(max_length=255, blank=True, default='')		# Position

class Building(models.Model):

	"""
		Django's Model to represent the building
		class in the MySQL database.
	"""

	code	= models.CharField(primary_key=True, max_length=4)	# Building's Code
	name	= models.CharField(max_length=255)			        # Building's Name

class Room(models.Model):

        """
                Django's Model to represent the room
                class in MySQL database.
        """

        id      = models.CharField(primary_key=True, max_length=255)     # Room's ID
        bd_code = models.ForeignKey(Building, on_delete=models.PROTECT) # Building Code
        level   = models.IntegerField()                                 # Room's level/Floor
        capacity= models.PositiveIntegerField()                         # Room's Capacity

class Course(models.Model):

	"""
		Django's Model to represent the course
		class in the MySQL Database.
	"""
	id	= models.CharField(primary_key=True, max_length=255)	# Course ID
	title	= models.CharField(max_length=255)				# Course's Title
	school	= models.CharField(max_length=255)				# School which owns the Course

class Unit(models.Model):

	"""
		Django's Model to represent the unit
		class in the MySQL database.
	"""

	code	= models.CharField(primary_key=True, max_length=255)		# Unit's code
	title 	= models.CharField(max_length=255)						# Unit Title
	credits = models.PositiveIntegerField()							# Unit's max credits
	image = models.CharField(max_length=255, default='default.jpg')

class Teaching_Period(models.Model):

	"""
		Django's Model to represent the teaching period
		class in the MySQL database.
	"""

	id 	= models.CharField(primary_key=True, max_length=255)	# Teaching Period ID
	name	= models.CharField(max_length=255)				# Teaching Period Name
	st_date	= models.DateField()							# Starting Date
	en_date	= models.DateField()							# Ending Date
