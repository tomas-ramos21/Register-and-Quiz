#!/bin/bash

# Author: Tomas Aleixo Ramos
# Purpose: Run commands which permit user to install all necessary dependencies.
# Date: 23-03-2019

# Installing Conda
$(echo "wget https://repo.anaconda.com/archive/Anaconda3-2018.12-Linux-x86_64.sh")
$(echo "bash Anaconda3-2018.12-Linux-x86_64.sh")

# Prepare Bash Shell to execute conda
$(echo "sudo ln -s /home/$USER/anaconda3/etc/profile.d/conda.sh /etc/profile.d/conda.sh")

# Install and activate conda enviroment
$(echo "conda env create -f environment.yml")
$(echo "conda activate regquiz")

# Install PIP dependencies
$(echo "sudo pip install -r requirements.txt")

# Create database tables and perform migrations
$(echo "python manage.py migrate auth")
$(echo "python manage.py migrate --run-syncdb")
$(echo "python manage.py migrate")
$(echo "python manage.py makemigrations")

# Create Django's Default Super User
$(echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@reg_and_quiz.com', 'imadmin')" | python manage.py shell)
