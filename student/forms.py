from django import forms

class codeForm(forms.Form): 
    code = forms.CharField(label='question_code', max_length=20)
    