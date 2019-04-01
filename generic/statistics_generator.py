import csv
import pandas as pd
from django.http import StreamingHttpResponse
from administrative.models import Teaching_Period, Unit, Course, Room, Building
from lecturer.models import Teaching_Day, Class, Published_Question
from student.models import Student, Answer

class stat_generator:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        return value

def csv_transfer(rows):
    pseudo_buffer = stat_generator()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="my_stats.csv"'
    return response

def room_usage_csv(room, period):

    # CSV columns
    dates    = []
    rooms    = []
    class_id = []
    std_amnt = []
    room_cap = []
    usage    = []
    period   = []

    t_days = list(Teaching_Day.objects.filter(r_id=Room))
    for day in t_days:
        class_item = Class.objects.filter(id=day.c_id).first()
        student_amount = Student.objects.filter(s_class=class_item).count()
        date = str(day.date_td.date())
        class_name = str(class_item.unit_id.code) + str(class_item.code)

        dates.append(str(date))
        rooms.append(str(room.id))
        room_cap.append(str(room.capacity))
        std_amnt.append(str(student_amount))
        class_id.append(str(class_name))
        period.append(str(period.id))
        usage.append(str(student_amount/room.capacity))

    data = { 'Date': dates,
             'Room': rooms,
             'Class': class_id,
             'Amount Students': std_amnt,
             'Room Capacity': room_cap,
             'Usage Percentage': usage,
             'Teaching Period': period }

    df = pd.DataFrame(data)
    rows = df.values.tolist()
    rows.insert(0, df.columns.tolist())
    return rows

def room_usage_csv_all(period):

    data = []
    rooms = list(Room.objects.all())
    for room in rooms:
        gen_data = room_usage_csv(room, period)
        if len(data) == 0:
            for row in gen_data:
                data.append(row)
        else:
            for row in gen_data[1:]:    # Doesn't add the header
                data.append(row)
    return data


def course_attendance_csv(period, course):

    # CSV columns
    unit               = []
    classes_r          = []
    periods            = []
    questions          = []
    answer_count       = []
    student_count      = []
    attendance_percent = []
    dates              = []

    # Obtain all classes for the given course and period
    units = Unit.objects.filter(course_id=course)
    classes = list(Class.objects.filter(t_period=period).filter(unit_id__in=units))

    for cls in classes:
        published_questions = list(Published_Question.objects.filter(q_class=cls))
        students = Student.objects.filter(s_class=cls).count()
        class_name = str(cls.unit_id.code) + str(cls.code)



        if students == 0 or len(published_questions) == 0:
            continue

        for question in published_questions:
            answers = Answer.objects.filter(q_id=question).count()
            attendance = answers/students
            date = question.tm_stmp.date()
            questions.append(str(question.code))
            answer_count.append(str(answers))
            attendance_percent.append(str(attendance))
            dates.append(str(date))
            unit.append(str(cls.unit_id.code))
            classes_r.append(class_name)
            periods.append(str(period.id))
            student_count.append(str(students))

        data = { 'Dates': dates,
                 'Classes': classes_r,
                 'Units': units,
                 'Teaching Period': periods,
                 'Question Code': questions,
                 'Answer Count': answer_count,
                 'Student Count': student_count,
                 'Attendance Percent': attendance_percent }

        df = pd.DataFrame(data)
        rows = df.values.tolist()
        rows.insert(0, df.columns.tolist())
        return rows

def course_attendance_csv_all(period):

    data = []
    courses = list(Course.objects.all())
    for course in courses:
        gen_data = course_attendance_csv(course, period)
        if len(data) == 0:
            for row in gen_data:
                data.append(row)
        else:
            for row in gen_data[1:]:    # Doesn't add the header
                data.append(row)
    return data

def unit_attendance_csv(period, unit):

    # CSV columns
    classes_s          = []
    questions          = []
    student_count      = []
    answer_count       = []
    attendance_percent = []
    dates              = []
    units               = []
    periods            = []


    classes = list(Class.objects.filter(t_period=period).filter(unit_id=unit))
    if not classes:
        print('yubu')
    # Find all published questions and students assigned to a class
    for cls in classes:
        published_questions = list(Published_Question.objects.filter(q_class=cls))
        students = Student.objects.filter(s_class=cls).count()
        class_name = str(cls.unit_id.code) + str(cls.code)

        if students == 0 or len(published_questions) == 0:
            continue

        # For each question find the response percentage
        for question in published_questions:
            answers = Answer.objects.filter(q_id=question).count()
            attendance = answers/students
            date = question.tm_stmp.date()
            questions.append(str(question.code))
            answer_count.append(str(answers))
            attendance_percent.append(str(attendance))
            dates.append(str(date))
            units.append(str(cls.unit_id.code))
            classes_s.append(class_name)
            periods.append(str(period.id))
            student_count.append(str(students))

        data = { 'Dates': dates,
                 'Classes': classes_s,
                 'Units': units,
                 'Teaching Period': periods,
                 'Question Code': questions,
                 'Answer Count': answer_count,
                 'Student Count': student_count,
                 'Attendance Percent': attendance_percent }

        df = pd.DataFrame(data)
        rows = df.values.tolist()
        rows.insert(0, df.columns.tolist())
        return rows

def unit_attendance_csv_all(period):

    data = []
    units = list(Unit.objects.all())
    for unit in units:
        gen_data = unit_attendance_csv(unit, period)
        if len(data) == 0:
            for row in gen_data:
                data.append(row)
        else:
            for row in gen_data[1:]:    # Doesn't add the header
                data.append(row)
    return data

def class_attendance_csv(cls):

    # CSV columns
    classes_s          = []
    questions          = []
    student_count      = []
    answer_count       = []
    attendance_percent = []
    dates              = []
    unit               = []
    periods            = []

    published_questions = list(Published_Question.objects.filter(q_class=cls))
    students = Student.objects.filter(s_class=cls).count()

    if students == 0 or len(published_questions) == 0:
        return None

    # For each question find the response percentage
    for question in published_questions:
        answers = Answer.objects.filter(q_id=question).count()
        attendance = answers/students
        date = question.tm_stmp.date()
        class_name = str(cls.unit_id.code) + str(cls.code)

        unit.append(str(cls.unit_id.code))
        classes_s.append(class_name)
        periods.append(str(cls.t_period.id))
        student_count.append(str(students))
        questions.append(str(question.code))
        answer_count.append(str(answers))
        attendance_percent.append(str(attendance))
        dates.append(str(date))

    data = { 'Dates': dates,
             'Classes': classes_s,
             'Units': unit,
             'Teaching Period': periods,
             'Question Code': questions,
             'Answer Count': answer_count,
             'Student Count': student_count,
             'Attendance Percent': attendance_percent }

    df = pd.DataFrame(data)
    rows = df.values.tolist()
    rows.insert(0, df.columns.tolist())
    return rows

def class_attendance_csv_all(period):

    data = []
    classes = list(Class.objects.filter(t_period=period))
    for cls in classes:
        gen_data = class_attendance_csv(cls)
        if len(data) == 0:
            for row in gen_data:
                data.append(row)
        else:
            for row in gen_data[1:]:    # Doesn't add the header
                data.append(row)
    return data
