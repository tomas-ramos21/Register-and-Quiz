import datetime
import itertools
from plotly.offline import plot
from plotly.graph_objs import Bar
from lecturer.models import Published_Question, Class
from administrative.models import Teaching_Period
from student.models import Answer

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

    x = []
    y = []
    for (key1,val1), (key2,val2) in zip(question_count.items(), answer_count.items()):
        x.append(key1)
        y.append(val1/val2)

    plot_div = plot([Scatter(x=x, y=y, line=dict(color='rgba(204,0,0)', opacity=0.8))])
    return plot_div
