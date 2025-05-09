from django.urls import path
from . import views


urlpatterns = [
    path('home/',views.home,name='home'),
    
    path('notes/',views.notes,name='notes'),
    path('delete_note/<int:pk>/',views.delete_note,name='delete_note'),
    path('detailView/<int:pk>/',views.NotesDetailview.as_view(),name='detail_notes'),
    
    path('homework/',views.homework,name='homework'),
    path('update_homework/<int:pk>/',views.update_homework,name='update_homework'),
    path('delete_homework/<int:pk>/',views.delete_homework,name='delete_homework'),
    
    path('youtube/',views.youtube,name='youtube'),
    
    path('todo/',views.todo,name='todo'),
    path('updatetodo/<int:pk>/',views.updatetodo,name='todo_update'),
    path('deletetodo/<int:pk>/',views.tododelete,name='delete_todo'),
    
    path('books/',views.books,name='books'),
    
    path('dictionary/',views.dictionary,name='dictionary'),
    
    path('wikipedia/',views.wiki,name='wikipedia'),
    
    path('conversion/',views.conversion,name='conversion'),
    
    path('logout/',views.log_out,name='logout'),
     
    
]