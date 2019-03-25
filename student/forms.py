from django import forms

class codeForm(forms.Form): 
    code = forms.CharField(label='Question Code', max_length=20)
    