from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import *
import requests
import wikipedia
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

#for creating notes and updating tables
@login_required
def notes(request):
    if request.method=='POST':
        form=Notesform(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            
            messages.success(request,f'Notes added from {request.user.username} successfully')
    else:
        form=Notesform()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)

#delete notes
@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes') 

#expanding notes part using generic and detailview 
class NotesDetailview(generic.DetailView):
    model=Notes
    
#creating the homework form and add to the tables
@login_required
def homework(request):
    if request.method=='POST':
        form=Homeworkform(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homework=Homework(user=request.user,subject=request.POST['subject'],title=request.POST['title'],description=request.POST['description'],due=request.POST['due'],is_finished=finished)
            homework.save()
            messages.success(request,f'data added from {request.user.username} successfully!!')
    else:
        form=Homeworkform()

    homework=Homework.objects.filter(user=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    context={'homeworks':homework,'homework_done':homework_done,'form':form}
    return render(request,'dashboard/homework.html',context)
 
#for updating the status like clicking the checkbox
@login_required
def update_homework(request,pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished==True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')
 
@login_required   
def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')

@login_required
def youtube(request):
    if request.method=='POST':
        form=Dashboardform(request.POST)
        text=request.POST['text']   # is retrive the values of the text field form POST request data
        video=Search(text,limit=5)  # for search related videos in youtube and taking the input field as text and here we have to set limt also 
        result_list=[]
        for i in video.result()['result']:     # for iterate the result and storing the result in i
            result_dict={                      # storing the data in dictionary format
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail': i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc=''                               # taken empty string  for adding description in string format
            if i['descriptionSnippet']:             # if description is there we can use if condition
                for j in i['descriptionSnippet']:   # if more than 2 description is there we can iterate the loop 
                    desc+=j['text']                # j['text'] is accessing the value from text and add to desc  
            result_dict['description']=desc         # desc description is store to the result_dict
            result_list.append(result_dict)         # and finally appended the  dictionary result in empty list
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
     
    else:                                        #  '''in this case the form is not a post method this else block 
        form=Dashboardform()                         #    wiil be execucated and display the form object '''
    context={'form':form}
    return render(request,'dashboard/youtube.html',context)


# creating todo function
@login_required
def todo(request):
    if request.method=='POST':
        form=Todoform(request.POST)  # for  creating todoform 
        if form.is_valid():
            try:                  # for checking existing value is finished or not
                finished=request.POST['is_finished']   # get is_finished from models 
                if finished =='on':   
                    finished=True
                else:
                    finished=False
            except:
                finished=False     #if try block any catches exeption  this block is execute
                    
            todo=Todo(user=request.user,title=request.POST['title'],is_finished=finished) 
            todo.save() # for creating new instance of django model
            messages.success(request,f'task added from {request.user.username} successfully!!')
    else:
            form=Todoform()            
    todo=Todo.objects.filter(user=request.user)  # this is for logged-in user for authentication
    
    # for checking length of collections(todo) if tables contains any data the false will execute
    if len(todo)==0:            
        todos_done=True
    else:
        todos_done=False
    context={'todos':todo,'form':form,'todos_done':todos_done} 
           
    return render(request,'dashboard/todo.html',context)

#update todo
@login_required
def updatetodo(request,pk=None):
    todo=Todo.objects.get(id=pk)
    '''its checking whether status is completed or not if its not checked  we can click checkbox and visaversa
     its updated in database aswell'''
    if todo.is_finished==True:
        todo.is_finished=False
    else:
        todo.is_finished=True
    todo.save()
    return redirect('todo')

#delete todo
@login_required
def tododelete(request,pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')
    
 
 # creating book function 
@login_required  
def books(request):
    if request.method=='POST':
        form=Dashboardform(request.POST)
        text=request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        r=requests.get(url) # clling requests of url and storing in r
        answer=r.json() #requesting url in the json form
        result_list=[]
        for i in range(10): # its iterates the loop 10 times and display 10 books names
            result_dict={
                # ['valumeInfo'] is used to extract title of the book  from valueInfo
                #['items'][i] is used to accesses the i-th book in the item list
                'title':answer['items'][i]['volumeInfo']['title'],    
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('averageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks',{}).get('thumbnail'),
                 
                'preview':answer['items'][i]['volumeInfo'].get('previewLink')
                
            }
            result_list.append(result_dict)  # for appending the data of result_dict to result_list
            context={'form':form,'results':result_list}
        return render(request,'dashboard/books.html',context)
            
    else:
        form=Dashboardform()
    context={'form':form}
    return render(request,'dashboard/books.html',context)

# creating dictionary function
@login_required
def dictionary(request):
    if request.method=='POST':
        form=Dashboardform(request.POST) 
        text=request.POST['text']   # for posting the user text 
        # text represents the user enter the data  and appending to the url
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        r=requests.get(url)   # for getting url request 
        answer=r.json()    # result coverting to json format
        # try block extract a specific data from the answer object which is json response from api
        try: 
            phonetics=answer[0]['phonetics'][0]['text']
            audio=answer[0]['phonetics'][0]['audio']
            definition=answer[0]['meanings'][0]['definitions'][0]['definition']
            example=answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms=answer[0]['meanings'][1]['definitions'][1]['synonyms']
            context={
                    'form':form,
                    'input':text,
                    'phonetics':phonetics,
                    'audio':audio,
                    'definition':definition,
                    'example':example,
                    'synonyms':synonyms
            }
            print(text,context)
        except:
            context={
                'form':form,     #if data is not found  that time it will display empty 
                'input':''
            }
        return render(request,'dashboard/dictionary.html',context)
    else:
        form=Dashboardform()
    context={'form':form}
    return render(request,'dashboard/dictionary.html',context)

#creating wikipedia function
@login_required
def wiki(request):
    if request.method=='POST':
        form=Dashboardform(request.POST)
        text=request.POST['text']
        # here imported wikipedia, and this is fetch specific wikipedia page for user text
        search=wikipedia.page(text)  
        # this context dictionary consoledate all relevent data and passes to the  html template   
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
            
        }
        return render(request,'dashboard/wiki.html',context)
    else:
        form=Dashboardform()
        context={'form':form}
    return render(request,'dashboard/wiki.html',context)

@login_required
def conversion(request):
    if request.method=='POST':
        form=Conversionform()
        # here if measurement is length then we have to take that lengthform
        if request.POST['measurement']=='length': 
            measurement_form=Conversionlengthform()
            context={
                'form':form,
                'm_form':measurement_form,
                'input':True    
            }
            # here if input is there in post method  then it wiil take  measure1 and 2 for conversion
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                # if input is not null
                if input and int(input)>0:
                    if first=='yard' and second=='foot':
                        answer=f'{input} yard={int(input)*3} foot' # converting yard to foot
                    if first=='foot' and second=='yard':
                        answer=f'{input} foot={int(input)/3} yard' #converting foot to yard
                        
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                }
                
     # here if measurement is mass then we have to take that lengthform
        if request.POST['measurement']=='mass': 
            measurement_form=Conversionmassform()
            context={
                'form':form,
                'm_form':measurement_form,
                'input':True    
            }
            # here if input is there in post method  then it wiil take  measure1 and 2 for conversion
            if 'input' in request.POST:
                first=request.POST['measure1']
                second=request.POST['measure2']
                input=request.POST['input']
                answer=''
                # if input is not null
                if input and int(input)>0:
                    if first=='pound' and second=='kilogram':
                        answer=f'{input} pound={int(input)*0.453592} kilograsm' # converting pound to kg
                    if first=='kilogram' and second=='pound':
                        answer=f'{input} kilogram={int(input)*2.2062} pound' #converting kg to pound
                        
                context={
                    'form':form,
                    'm_form':measurement_form,
                    'input':True,
                    'answer':answer
                } 
                        
                
    else:
                
        form=Conversionform()
        context={'form':form}
    return render(request,'dashboard/conversion.html',context)

 
def user_rigister(request):
    if request.method=='POST':
        form=Userrigisterform(request.POST)
        if form.is_valid():
            form.save()
            # this is used for displaying account creation message
            username=form.cleaned_data.get('username')
            messages.success(request,f'Account created for{username} successfuly!!')
            
            return redirect('login')
            
            
    else:
            
        form=Userrigisterform()
    context={'form':form}
    return render(request,'dashboard/register.html',context)
@login_required   
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    todos=Todo.objects.filter(is_finished=False,user=request.user)
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    if len(todos)==0:
        todos_done=True
    else:
        todos_done=False
    context={
        'homeworks':homeworks,
        'todos':todos,
        'homework_done':homework_done,
        'todos_done':todos_done
        
    }
    return render(request,'dashboard/profile.html',context)

def log_out(request):
    logout(request)
    return render(request,'dashboard/logout.html')
 