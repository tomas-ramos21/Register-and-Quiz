import datetime
import itertools
from plotly.offline import plot
from plotly.graph_objs import Bar, Scatter
from lecturer.models import Published_Question, Class, Teaching_Day, Published_Question
from administrative.models import Teaching_Period, Room, Unit, Course
from student.models import Answer, Student

def answer_graph(question_code):

    published = Published_Question.objects.filter(code=question_code).first()

    y = []       # Answers count
    x = []       # Answers

    y.append(Answer.objects.filter(q_id=published).filter(ans=published.question.ans_1).count())
    y.append(Answer.objects.filter(q_id=published).filter(ans=published.question.ans_2).count())
    y.append(Answer.objects.filter(q_id=published).filter(ans=published.question.ans_3).count())
    y.append(Answer.objects.filter(q_id=published).filter(ans=published.question.ans_4).count())

    x.append('A')
    x.append('B')
    x.append('C')
    x.append('D')

    color   = ['rgba(58,135,173)', 'rgba(204,0,0)', 'rgba(250,178,11)', 'rgba(85,152,33)']
    line    = ['rgba(0,0,0)', 'rgb(0,0,0)', 'rgb(0,0,0)', 'rgb(0,0,0)']
    line_w  = [1.5, 1.5, 1.5, 1.5]

    plot_div = plot([Bar(x=x,y=y, marker=dict(color=color, line=dict(color=line, width=line_w)))], output_type='div')

    return plot_div

def attendance_graph(unit, period, student):

    possible_classes = list(Class.objects.filter(unit_id=unit).filter(t_period=period))
    student_classes  = list(student.s_class.all())
    stats_class = None

    for cls in student_classes:
        if cls in possible_classes:
            stats_class = cls
            break

    published = list(Published_Question.objects.filter(q_class=cls))
    question_count = {}
    answer_count = {}
    for question in published:
        date = question.tm_stmp.date()
        ans = Answer.objects.filter(s_id=student).filter(q_id=question).first()
        if date not in question_count:
            question_count[date] = 1
            answer_count[date] = 0
        else:
            question_count[date] += 1

        if ans != None:
            answer_count[date] += 1

    x = []       # Dates
    y = []       # Answer Percentage

    for (key1,val1), (key2,val2) in zip(question_count.items(), answer_count.items()):
        x.append(key1)
        y.append(val2/val1)

    plot_div = plot([Scatter(x=x, y=y, line=dict(color='rgba(204,0,0)'))], output_type='div')
    return plot_div

def admin_attendance_graph(period, granularity, text_selection):

    selected_period = Teaching_Period.objects.filter(id=period).first()

    granularity = granularity.lower()
    x = []
    y = []

    if granularity == 'course':
        if text_selection.lower() == 'all':
            courses = list(Course.objects.all())
            labels = []
            for course in courses:
                _x, _y = get_course_attendance(selected_period, course)
                x.append(_x)
                y.append(_y)
                labels.append(str(course.id))
            graphs = []
            for x_val, y_val, label in zip(x, y, labels):
                graphs.append(Scatter(x=x_val,y=y_val,name=label))
            plot_div = plot(graphs, output_type='div')
        else:
            course = Course.objects.filter(id=text_selection).first()
            if course is None:
                return False
            x, y = get_course_attendance(selected_period, course)
            plot_div = plot([Scatter(x=x,y=y,name=course.id)], output_type='div')

    if granularity == 'unit':
        if text_selection.lower() == 'all':
            units = list(Unit.objects.all())
            labels = []
            for unit in units:
                _x, _y = get_unit_attendance(selected_period, unit)
                x.append(_x)
                y.append(_y)
                labels.append(str(unit.code))
            graphs = []
            for x_val, y_val, label in zip(x, y, labels):
                graphs.append(Scatter(x=x_val,y=y_val,name=label))
            plot_div = plot(graphs, output_type='div')
        else:
            unit = Unit.objects.filter(code=text_selection).first()
            if unit is None:
                return False
            x, y = get_unit_attendance(selected_period, unit)
            plot_div = plot([Scatter(x=x,y=y,name=unit.code)], output_type='div')

        if granularity == 'class':
            if text_selection.lower() == 'all':
                t_period = Teaching_Period.objects.filter(id=selected_period).first()
                classes = list(Class.objects.filter(t_period=t_period))
                labels = []
                for cls in classes:
                    _x, _y = get_class_attendance(cls)
                    x.append(_x)
                    y.append(_y)
                    labels.append(str(cls.unit_id.code) + ' ' + str(cls.code))
                graphs = []
                for x_val, y_val, label in zip(x, y, labels):
                    graphs.append(Scatter(x=x_val,y=y_val,name=label))
                plot_div = plot(graphs, output_type='div')
            else:
                t_period = Teaching_Period.objects.filter(id=selected_period).first()
                unit = Unit.Objects.filter(code=text_selection[:len(text_selection)-2]).first()
                cls = Class.objects.filter(code=text_selection[-1:]).filter(t_period=t_period).filter(unit).first()
                if cls == None or unit == None or t_period == None:
                    return False
                x, y = get_course_attendance(selected_period, unit)
                label = str(cls.unit_id.code) + ' ' + str(cls.code)
                plot_div = plot([Scatter(x=x,y=y,name=label)], output_type='div')

    return plot_div



def get_course_attendance(period, course):
    date_attendance = {}

    # Obtain all classes for the given course and period
    units = Unit.objects.filter(course_id=course)
    classes = list(Class.objects.filter(t_period=period).filter(unit_id__in=units))

    # Find all published questions and students assigned to a class
    for cls in classes:
        published_questions = list(Published_question.object.filter(q_class=cls))
        students = Student.objects.filter(s_class=cls).count()
        if students == 0 or len(published_questions) == 0:
            continue

        # For each question find the response percentage
        for question in published_questions:
            answers = Answer.objects.filter(q_id=question).count()
            attendance = answers/students
            date = question.tm_stmp.date()

            # If records for the given date exist merge them, otherwise add entry
            if date in date_attendance:
                date_attendance[date].append(attendance)
            else:
                date_attendance[date] = [attendance]

    x = []        # Dates
    y = []        # Average attendance percentages

    for key, val in date_attendance.items():
        x.append(key)
        y.append(sum(val)/len(val))

    return x, y

def get_unit_attendance(period, unit):
    date_attendance = {}
    classes = list(Class.objects.filter(t_period=period).filter(unit_id=unit))

    # Find all published questions and students assigned to a class
    for cls in classes:
        published_questions = list(Published_Question.objects.filter(q_class=cls))
        students = Student.objects.filter(s_class=cls).count()
        if students == 0 or len(published_questions) == 0:
            continue

        # For each question find the response percentage
        for question in published_questions:
            answers = Answer.objects.filter(q_id=question).count()
            attendance = answers/students
            date = question.tm_stmp.date()

            # If records for the given date exist merge them, otherwise add entry
            if date in date_attendance:
                date_attendance[date].append(attendance)
            else:
                date_attendance[date] = [attendance]

    x = []        # Dates
    y = []        # Average attendance percentages

    for key, val in date_attendance.items():
        x.append(key)
        y.append(sum(val)/len(val))

    return x, y

def get_class_attendance(cls):
    date_attendance = {}
    published_questions = list(Published_question.object.filter(q_class=cls))
    students = Student.objects.filter(s_class=cls).count()
    x = []
    y = []
    if students == 0 or len(published_questions) == 0:
        return x, y

    # For each question find the response percentage
    for question in published_questions:
        answers = Answer.objects.filter(q_id=question).count()
        attendance = answers/students
        date = question.tm_stmp.date()

        # If records for the given date exist merge them, otherwise add entry
        if date in date_attendance:
            date_attendance[date].append(attendance)
        else:
            date_attendance[date] = [attendance]

        for key, val in date_attendance.items():
            x.append(key)
            y.append(sum(val)/len(val))

        return x, y

def admin_room_usage(period, selection):
    selected_period = Teaching_Period.objects.filter(id=period).first()
    selection = selection.upper()
    x = []
    y = []

    if selection.lower() == 'all':
        rooms = list(Room.objects.all())
        labels = []
        for room in rooms:
            _x, _y = get_room_attendance(room, selected_period)
            x.append(_x)
            y.append(_y)
            labels.append(room.id)
        graphs = []
        for x_val, y_val, label in zip(x, y, labels):
            graphs.append(Scatter(x=x_val,y=y_val,name=label))
        plot_div = plot(graphs, output_type='div')
    else:
        room = Room.objects.filter(id=selection).first()
        if room is None:
            return None
			
        x, y = get_room_attendance(room, selected_period)
        plot_div = plot([Scatter(x=x,y=y,name=room.id)], output_type='div')
    return plot_div

def get_room_attendance(room, period):
    t_days = list(Teaching_Day.objects.filter(r_id=room))
    print(Teaching_Day.objects.filter(r_id=room).first())
   
    room_usage = {}
    for day in t_days:
        a_class = Class.objects.filter(id=day.c_id.id).first()

        student_amount = Student.objects.filter(s_class=a_class).count()
        date = str(day.date_td)
        if date in room_usage:
            room_usage[date].append(student_amount/room.capacity)
        else:
            room_usage[date] = [student_amount/room.capacity]

    x = []      # Dates
    y = []      # Max Average Attendance

    for key, val in room_usage.items():
        y.append(sum(val)/len(val))
        x.append(key)

    return x, y
