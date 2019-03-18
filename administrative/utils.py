import os
import csv
from .models import Employee
from django.contrib.auth import authenticate
from django.contrib import admin
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.conf import settings
User = get_user_model()

def register_lecturer(csv_path):

    columns = ['id', 'password', 'first_name', 'last_name', 'email', 'department', 'position']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):  # For each row
            if idx != 0:                    # If row isn't the header
                crt_dict = {}
                for column in columns:
                    crt_dict[column] = row[column]
                employee = User()
                employee.set_password(crt_dict['password'])
                employee.username = crt_dict['id']
                employee.first_name = crt_dict['first_name']
                employee.last_name = crt_dict['last_name']
                employee.email = crt_dict['email']
                employee.dpt = crt_dict['department']
                employee.position = crt_dict['position']
                employee.save()


                # Save Employee object into the database
                # staff = Employee.objects.create()

    os.remove(csv_path)

def register_student(csv_path):

    columns = ['id', 'password', 'first_name', 'last_name', 'email']

    with open(csv_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file, fieldnames=columns)

        for idx, row in enumerate(reader):
            if idx != 0:
                for column in columns:
                    print(row[column])
