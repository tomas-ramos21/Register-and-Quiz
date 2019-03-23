# Author: Tomas Ramos
# Date: 20-03-2019
# Purpose: Define functions providing extra utility to the administrative app.
# Last Modified By: Madyarini
# Last Modified Date: 20-03-2019

import os
import csv
from django.http import HttpResponseRedirect, HttpResponse
from login.models import Employee, Student
from administrative.models import Building, Room
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from typing import Dict, Tuple


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

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email',
               'department',
               'position']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):  # For each row
            if idx != 0:                    # If row isn't the header
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
                employee = Employee(user=user,
                                    dpt=crt_dict['department'],
                                    pstn=crt_dict['position'])
                employee.save()

def register_student(csv_path: str) -> None:
    """
        Registers students in the platform.

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

    columns = ['id',
               'password',
               'first_name',
               'last_name',
               'email']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

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

def get_context(user) -> Dict:
    context_dict = {'name_header' : user.first_name,
                    'name_menu'   : user.first_name + ' ' + user.last_name }
    return context_dict

def find_user(username:str) -> Tuple:

    # Find user object
    user = User.objects.filter(username=username).first()
    # If user doesn't exist
    if user is None:
        return (None, None)

    # Find student object
    student	= Student.objects.filter(user=user).first()
    # If student exists
    if not student is None:
        return (student, 'student')

    # Find employee object
    employee = Employee.objects.filter(user=user).first()
    # if employee exists
    if not student is None:
        return (employee, 'employee')

def register_room(csv_path: str) -> None:

    columns = ['id',
               'building_code',
               'level',
               'capacity']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                room = Room(id=crt_dict['id'],
                            bd_code=crt_dict['building_code'],
                            level=crt_dict['level'],
                            capacity=crt_dict['capacity'])
                room.save()

def register_building(csv_path:str) -> None:

    columns = ['code','name']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                building = Building(code=crt_dict['code'], name=crt_dict['name'])
                building.save() 
