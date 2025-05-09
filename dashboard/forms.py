﻿from django import forms
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
        
class Conversionform(forms.Form):
    CHOICES=[('length','Length'),('mass','Mass')]
    measurement=forms.ChoiceField(choices=CHOICES,widget=forms.RadioSelect)
        
class Conversionlengthform(forms.Form):
    CHOICES=[('yard','Yard'),('foot','Foot')]
    input=forms.CharField(required=False,label=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    
    measure1=forms.CharField(label='', widget=forms.Select(choices=CHOICES))
    
    measure2=forms.CharField(label='',widget=forms.Select(choices=CHOICES))
    
    
class Conversionmassform(forms.Form):
    CHOICES=[('pound','Pound'),('kilogram','Kilogram')]
    input=forms.CharField(label=False,required=False,widget=forms.TextInput(
        attrs={'type':'number','placeholder':'Enter the Number'}
    ))
    
    measure1=forms.CharField(label='',widget=forms.Select(choices=CHOICES))
    
    measure2=forms.CharField(label='',widget=forms.Select(choices=CHOICES))

class Userrigisterform(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['fullname','email']