from django import forms

class codeForm(forms.Form): 
    code = forms.IntegerField(label='Question Code')
    