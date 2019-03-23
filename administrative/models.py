from django.db import models

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
