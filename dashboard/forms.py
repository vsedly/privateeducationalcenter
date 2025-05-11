from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class Notesform(forms.ModelForm):
    class Meta:
        model=Notes
        fields=['title','description']
        
class DateInput(forms.DateInput):
    input_type='date'
    
class Homeworkform(forms.ModelForm):
    class Meta:
        model=Homework
        widgets={'due':DateInput()}
        fields=['subject','title','description','due','is_finished']
        
class Dashboardform(forms.Form):
    text=forms.CharField(max_length=200,label='Enter your Search')
        
class Todoform(forms.ModelForm):
    class Meta:
        model=Todo
        fields=['title','is_finished']
        

class Userrigisterform(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['fullname','email']

        from django import forms
from .models import StudentSchedule

class StudentScheduleForm(forms.ModelForm):
    class Meta:
        model = StudentSchedule
        fields = ['subject', 'start_time', 'end_time', 'date', 'description']