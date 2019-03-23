# Reg & Quiz
Final year project repository for Murdoch University.

### File Headers
Although git makes it easy to collaborate it will be hard to keep track of the changes everyone does per file, as well as when those changes happen. Therefore, upon the creation of each file the following header should be added:

1. #@Author: my name
2. #@Date: creation date
3. #@Purpose: File's purpose
4. #@Last Modified by: my name
5. #@Last Modified Date: change date


### Django Apps
Django works with apps, which may includes several modules (.py files). The work will be split among the team through the apps. For example, one individual may be responsible for the student app of the website which allows students to perform their respective activites on the website.

### Python Environment
Conda will be used to install python packages and everyone should have it installed on their local machine. In order to avoid problems between versions of these packages we will all use the same environment. This means the **.yml** file in the repository has all packages installed and passing this file to conda will allow to replicate the same environment. Unfortunately conda doesn't have all packages, so some of them have to be installed with **pip**. However, this is easy to do since it has the same system in which a file with the dependencies is passed and pip installs them for you. For this project this file is called **requirements.txt**. More information on how to do this is in the link below:

[Conda Enviroments](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)

[Pip Requirements](https://pip.pypa.io/en/stable/reference/pip_freeze/)

### Repository Structure
As mentioned before the project will be organised using apps. In order to permit a swift development and reduce constraints follow the structure below.

```python
>  Reg_-_Quiz
>     |
>     |-Administrative   # App's Structure
>     |   |-__init__.py
>     |   |-admin.py
>     |   |-apps.py
>     |   |-models.py
>     |   |-tests.py
>     |   |-urls.py
>     |   |-views.py
>     |
>     |-Lecturer
>     |-Login
>     |-Student
>     |
>     |-dummy_data
>     |   |-Student_Dummy.csv
>     |   
>     |-generic        # Utility functions
>     |   |-utils.py
>     |
>     |-media          # Media Files
>     |   |-image.jpeg
>     |
>     |-reg_and_quiz   # Main Website Settings
>     |   |-__init__.py
>     |   |-settings.py
>     |   |-urls.py
>     |   |-wsgi.py
>     |
>     |-static         # Static Files (e.g. JavaScript)
>     |-templates      # HTML Templates
```

### Documenting Python Code
Reading another individuals python code can be hard, due to the fact we don't have any clue what type the function is expecting. Moreover, python doesn't prevent you from calling functions even if the types are not the ones expected for the function.

In order to facilitate this we will use **"type hints"**, which still don't enforce a type for a parameter but atleast provide some information regarding the expected inputs and output. Lastly, a small string should be at the start of every function to explain it. Later this string can be printed by python to explain exactly what it does.

Check the links and code below for examples:

[Python's Docstring](https://www.pythonforbeginners.com/basics/python-docstrings)

[Python's Type Hints](https://docs.python.org/3/library/typing.html)

```python
# Undocumented
def my_function(parameter_1, parameter_2):
      return parameter_1 + parameter_2

# Documented
# 1. We know the expected parameter types
# 2. We know the expected return type denoted by the arrow
# 3. We have a small portion of text that documents the function
def my_function(parameter_1: int, parameter_2: int) -> int:
      """
          This functions adds two numbers
          
          Parameters
          ----------
          parameter_1: int
              explain the parameter
          parameter_2: int
              explain the parameter
          
          Returns
          ---------
          Explain the return value
      """
      return parameter_1 + parameter_2
```
