# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Define functions providing extra utility to the administrative app.
# Last Modified By: Madyarini
# Last Modified Date: 20-03-2019

import os
import csv
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from student.models import Student
from lecturer.models import Question, Published_Question, Class, Topic
from administrative.models import Building, Room, Employee, Unit, Course, Teaching_Period
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from typing import Dict, Tuple

from generic.statistics_generator import class_attendance_csv, class_attendance_csv_all, unit_attendance_csv, unit_attendance_csv_all, course_attendance_csv, course_attendance_csv_all, csv_transfer, room_usage_csv, room_usage_csv_all

def get_admin_context(user) -> Dict:
	admin = Employee.objects.filter(user=user).first()
	if admin is not None:
		user_dict = {
			'f_name': user.first_name,
			'fl_name': user.first_name + ' ' + user.last_name
		}
		return user_dict
	else:
		return {}


def get_lecturer_context(user) -> Dict:
	lect = Employee.objects.filter(user=user).first()
	if lect is not None:
		class_taught = Class.objects.filter(staff_id=lect)  # year?
		unit_list = [x.unit_id for x in class_taught]

		period_display = []

		t_period = [x.t_period.id.lower() for x in class_taught]

		for y in t_period:
			period = ''
			for letter in y:
				if letter == '-':
					letter = ', '
				period += letter
			period_display.append(period)

		class_display = list(zip(unit_list, period_display))
		user_dict = {
			'f_name': lect.user.first_name,
			'fl_name': lect.user.first_name + ' ' + lect.user.last_name,
			'position': lect.pstn.upper(),
			'class_display': class_display,
		}
		return user_dict
	else:
		return {}


def get_std_context(user):
	std = Student.objects.filter(user=user).first()
	if std is not None:
		enrolled_class = std.s_class.all()
		unit_list = [x.unit_id for x in enrolled_class]

		period_display = []

		t_period = [x.t_period.id.lower() for x in enrolled_class]

		for y in t_period:
			period = ''
			for letter in y:
				if letter == '-':
					letter = ', '
				period += letter
			period_display.append(period)

		class_display = list(zip(unit_list, period_display))
		user_dict = {
			'f_name': std.user.first_name,
			'fl_name': std.user.first_name + ' ' + std.user.last_name,
			'class_display': class_display,
		}
		return user_dict
	else:
		return {}


def register_employee(csv_path: str) -> None:
	"""
		Registers lecturers in the platform.
		Iterates over the rows of a CSV file
		collecting the information to be used
		for the account creation.
		Parameters
		----------
		csv_path: str
			String containing the path to the
			file.
		TODO
		----------
		1. Function do check the information
		used during creation is accurate.
	"""

	msg = ""
	columns = ['id', 'password', 'first_name', 'last_name', 'email', 'department', 'position']
	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, user_dict

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, user_dict

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):  # For each row
			if idx != 0:  # If row isn't the header
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				user = User()
				user.set_password(crt_dict['password'])
				user.username = crt_dict['id']
				user.first_name = crt_dict['first_name']
				user.last_name = crt_dict['last_name']
				user.email = crt_dict['email']
				user.save()
				employee = Employee(user=user, dpt=crt_dict['department'], pstn=crt_dict['position'])
				employee.save()
		return True, msg


def register_student(csv_path: str) -> None:
	"""
		Registers students in the platform.
		Iterates over the rows of a CSV file
		collecting the information to be used
		for the account creation.
		Parameters
		----------
		csv_path: str
			String containing the path to the file.
	"""
	msg = ""

	columns = ['id', 'password', 'first_name', 'last_name', 'email']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		# Start registering
		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				user = User()
				user.set_password(crt_dict['password'])
				user.username = crt_dict['id']
				user.first_name = crt_dict['first_name']
				user.last_name = crt_dict['last_name']
				user.email = crt_dict['email']
				user.save()
				student = Student(user=user)
				student.save()
		return True, msg


def validate_header(headers, file_headers):
	count = len(headers)
	for header in headers:
		if header in file_headers:
			count -= 1
	if count != 0:
		return False
	return True


def find_user(username: str) -> Tuple:
	# Find user object
	user = User.objects.filter(username=username).first()
	# If user doesn't exist
	if user is None:
		return (None, None)

	# Find student object
	student = Student.objects.filter(user=user).first()
	# If student exists
	if not student is None:
		return (student, 'student')

	# Find employee object
	employee = Employee.objects.filter(user=user).first()
	# if employee exists
	if not student is None:
		return (employee, 'employee')


def register_room(csv_path: str) -> None:
	msg = ""
	columns = ['id', 'building_code', 'level', 'capacity']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Headers
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				building = Building.objects.filter(code=crt_dict['building_code']).first()
				room = Room(id=crt_dict['id'], bd_code=building, level=crt_dict['level'], capacity=crt_dict['capacity'])
				room.save()
		return True, msg


def register_building(csv_path: str) -> None:
	msg = ""
	columns = ['code', 'name']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Headers
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				building = Building(code=crt_dict['code'], name=crt_dict['name'])
				building.save()
		return True, msg


def register_units(csv_path: str) -> None:
	msg = ""
	columns = ['code', 'title', 'credits', 'image']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Header
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				unit = Unit(code=crt_dict['code'], title=crt_dict['title'], credits=crt_dict['credits'],
							image=crt_dict['image'])
				unit.save()
		return True, msg


def register_courses(csv_path: str) -> None:
	msg = ""
	columns = ['id', 'title', 'school']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Header
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				course = Course(id=crt_dict['id'], title=crt_dict['title'], school=crt_dict['school'])
				course.save()
		return True, msg


def register_teaching_period(csv_path: str) -> None:
	msg = ""
	columns = ['id', 'name', 'start_date', 'end_date']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Header
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				teaching_period = Teaching_Period(id=crt_dict['id'], name=crt_dict['name'],
												  st_date=crt_dict['start_date'], en_date=crt_dict['end_date'])
				teaching_period.save()
		return True, msg


def register_questions(csv_path: str) -> None:
	msg = ""
	columns = ['unit',
			   'staff_id',
			   'title',
			   'question',
			   'answer_1',
			   'answer_2',
			   'answer_3',
			   'answer_4',
			   'topic']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Header
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				unit = Unit.objects.filter(code=crt_dict['unit']).first()
				topic = Topic.objects.filter(number=crt_dict['topic']).filter(unit_id=unit).first()
				user = User.objects.filter(username=crt_dict['staff_id']).first()
				lecturer = Employee.objects.filter(user=user).first()
				question = Question(text=crt_dict['question'],
									ans_1=crt_dict['answer_1'],
									ans_2=crt_dict['answer_2'],
									ans_3=crt_dict['answer_3'],
									ans_4=crt_dict['answer_4'],
									title=crt_dict['title'],
									topic_id=topic,
									staff_id=lecturer)
				question.save()
		return True, msg


def find_room(room_code):
	return Room.objects.filter(id=room_code).first()


def find_building(building_code):
	return Building.objects.filter(code=building_code).first()


def generate_random_code():
	# Generates random code for questions
	# Number has always 9 digits
	# So its easy to display like this      999-666-888
	code = random.randint(100000000, 999999999)
	if not Published_Question.objects.filter(code=code).first() is None:
		code = generate_random_code()
	return code


def publish_question(question, time: int, q_class) -> None:
	code = generate_random_code()
	publish = Published_Question(code=code,
								 question=question,
								 q_class=q_class,
								 minutes_limit=time)
	publish.save()
	return code


def register_class(user, csv_path: str):
	columns = ['unit',
			   'teaching_period',
			   'time_commitment',
			   'class_code']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Header
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]

				# Get Foreign Keys
				unit = Unit.objects.filter(code=crt_dict['unit']).first()
				t_period = Teaching_Period.objects.filter(id=crt_dict['teaching_period']).first()
				staff = Employee.objects.filter(user=user).first()
				if unit not in staff.units.all():
					msg = 'You are not allowed to create classes for this unit.'
					return False, msg

				existent_class = Class.objects.filter(unit_id=unit).filter(t_period=t_period).filter(
					code=crt_dict['class_code']).first()

				if existent_class is not None:
					msg = 'Class {} for unit {}, already exists in the given teaching period.'.format(
						crt_dict['class_code'], unit.code)
					return False, msg

				# Create class
				new_class = Class(unit_id=unit,
								  t_period=t_period,
								  staff_id=staff,
								  time_commi=crt_dict['time_commitment'],
								  code=crt_dict['class_code'])
				new_class.save()

	return new_class, msg


def add_students(user, csv_path: str):
	msg = ""
	columns = ['class code','teaching period','time commitment','id','action']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check Readers
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				user1 = User.objects.filter(username=crt_dict['id']).first()
				if user1 is not None :
					student = Student.objects.filter(user=user1).first()
					if student is not None:
						unit = crt_dict['class code'][:6]
						unit_item = Unit.objects.filter(code=unit).first()
						tp = Teaching_Period.objects.filter(id=crt_dict['teaching period']).first()
						if unit_item is not None and tp is not None :
							code = crt_dict['class code'][-1]
							class_obj = Class.objects.filter(unit_id=unit_item, time_commi=crt_dict['time commitment'], code=code, t_period=tp).first()
							emp = Employee.objects.filter(user=user).first()
							if class_obj.staff_id == emp:
								if class_obj is not None:
									act = crt_dict['action']
									if act == 'remove':
										student.s_class.remove(class_obj)
									elif act == 'add':
										student.s_class.add(class_obj)
									student.save()
								else:
									print('huhu')
		return True, msg


def register_topics( csv_path: str) -> None:
	msg = ""
	columns = ['number', 'name', 'unit']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check headers
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row) or len(row) < len(columns):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		# Start Registering
		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				unit = Unit.objects.filter(code=crt_dict['unit']).first()
				topic = Topic(number=crt_dict['number'], name=crt_dict['name'], unit_id=unit)
				topic.save()
		return True, msg


def extract_info_student(student):
	classes = list(student.s_class.all())
	courses = list(student.s_course.all())
	units = []
	for cls in classes:
		units.append(cls.unit_id)
	return classes, courses, units


def extract_info_lecturer(lecturer):
	classes = list(Class.objects.filter(staff_id=lecturer))
	units = []
	for cls in classes:
		units.append(cls.unit_id)
	return classes, units


def is_empty(row):
	lookups = (None, '', ' ')
	for cell in row:
		if cell in lookups:
			return True
	return False


def edit_units(csv_path: str):
	msg = ""
	columns = ['staff_id', 'unit', 'action']

	with open(csv_path, 'r') as csv_file:
		rows = list(csv.reader(csv_file))

		# Check headers
		if validate_header(columns, rows[0]) == False:
			msg = 'Headers are wrong, headers should be: {}'.format(columns)
			return False, msg

		# Check empty values
		for idx, row in enumerate(rows):
			if is_empty(row) or len(row) < len(columns):
				msg = 'File has an empty cell at index: {}'.format(idx)
				return False, msg

		# Checks all cells exist
		for idx, row in enumerate(rows):
			if len(row) < len(columns):
				msg = 'File has missing cells at index: {}'.format(idx)
				return False, msg

	with open(csv_path, 'r') as csv_file:
		reader = csv.DictReader(csv_file, fieldnames=columns)

		# Start Registering
		for idx, row in enumerate(reader):
			if idx != 0:
				crt_dict = {}
				for column in columns:
					crt_dict[column] = row[column]
				user = User.objects.filter(username=crt_dict['staff_id']).first()
				lecturer = Employee.objects.filter(user=user).first()
				unit = Unit.objects.filter(code=crt_dict['unit']).first()
				if crt_dict['action'].lower() == 'add':
					lecturer.units.add(unit)
				elif crt_dict['action'].lower() == 'remove':
					lecturer.units.remove(unit)
		return True, msg


def admin_attendance_csv(period, granularity, text_selection):
	selected_period = Teaching_Period.objects.filter(id=period).first()
	granularity = granularity.lower()
	data = []
	if granularity == 'course':
		if text_selection.lower() == 'all':
			data = course_attendance_csv_all(selected_period)
		else:
			course = Course.objects.filter(id=text_selection).first()
			if course is None:
				return False
			data = course_attendance_csv(selected_period, course)

	if granularity == 'unit':
		if text_selection.lower() == 'all':
			data = units_attendance_csv_all(selected_period)
		else:
			unit = Unit.objects.filter(code=text_selection).first()
			if unit is None:
				return False
			data = unit_attendance_csv(selected_period, unit)

	if granularity == 'class':
		if text_selection.lower() == 'all':
			t_period = Teaching_Period.objects.filter(id=selected_period).first()
			classes = list(Class.objects.filter(t_period=t_period))
			data = class_attendance_csv_all(selected_period)
		else:
			t_period = Teaching_Period.objects.filter(id=period).first()
			unit = Unit.objects.filter(code=text_selection[:len(text_selection) - 1]).first()
			cls = Class.objects.filter(code=text_selection[-1:]).filter(t_period=t_period).filter(unit_id=unit).first()

			if cls is None or unit is None or t_period is None:
				return False

			data = class_attendance_csv(cls)

	return csv_transfer(data)

def admin_space_csv(period, selection):
	selected_period = Teaching_Period.objects.filter(id=period).first()
	selection = selection.upper()
	data = []
	if selection.lower() == 'all':
		rooms = list(Room.objects.all())
		data = room_usage_csv_all(selected_period)
	else:
		room = Room.objects.filter(id=selection).first()
		if room is None:
			return None
		data = room_usage_csv(selection, selected_period)

	return csv_transfer(data)