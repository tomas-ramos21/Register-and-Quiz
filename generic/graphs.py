from plotly.offline import plot
from plotly.graph_objs import Bar
from lecturer.models import Published_Question
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
