import wikipedia 
from django.shortcuts import render, redirect
from .models import *
from .models import Notes
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests 
import wikipedia

# Create your views here.

def home(request):
    return render(request, "dashboard/home.html")

# Notes Section
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user,
                title=request.POST['title'],
                description=request.POST['description']
            )
            notes.save()
            messages.success(request, f"Notes added by {request.user.username} successfully.")
    else:
        form = NotesForm()

    notes = Notes.objects.filter(user=request.user)
    context = {'notes': notes, 'form': form}
    return render(request, 'dashboard/notes.html', context)

# Delete Notes
def delete_note(request, pk = None):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NotesDetailView(generic.DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'
    context_object_name = 'note'


# Homeworks Section
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(
                user = request.user, 
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due = request.POST['due'],
                is_finished = finished
                )
            homeworks.save()
            messages.success(request,f'Homework Added from {request.user.username}!!')
    else:
        form = HomeworkForm()

    homework = Homework.objects.filter(user=request.user)

    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {'homeworks' : homework, 'homeworks_done' : homework_done, 'form' : form}
    return render(request, 'dashboard/homework.html', context)


# is Homeworks finish
def update_homework(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

def delete_homework(request, pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


# Youtube Section
def youtube(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=40)
        result_list = []
        for i in video.result()['result']:
            result_dict = {
                'input' : text,
                'title' : i['title'],
                'duration' : i['duration'],
                'thumbnail' : i['thumbnails'][0]['url'],
                'channel' : i['channel']['name'],
                'link' : i['link'],
                'views' : i['viewCount']['short'],
                'published' : i['publishedTime'],
            }
            desc = ''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc += j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            contaxt = {
                'form' : form,
                'results' : result_list
            }
        return render(request, 'dashboard/youtube.html',contaxt)
    else:
        form = DashboardForm()

    contaxt = {'form' : form}
    return render(request, 'dashboard/youtube.html', contaxt) 


#Todo Section
def todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST["is_finished"]
                if finished == "on":
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished
            )
            todos.save()
            messages.success(request,f"Todo Added from {request.user.username}!!")
    else:
        form = TodoForm()

    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False
    contaxt = {
        'form' : form,
        'todos' : todo,
        'todos_done' : todos_done
    }
    return render(request, 'dashboard/todo.html', contaxt)

def update_todo(request,pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo') 

def delete_todo(request, pk=None):
    todo = Todo.objects.get(id=pk).delete()
    return redirect('todo')

# Books Section

def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title' : answer['items'][i]['volumeInfo']['title'],
                'subtitle' : answer['items'][i]['volumeInfo'].get('subtitle'),
                'description' : answer['items'][i]['volumeInfo'].get('description'),
                'count' : answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories' : answer['items'][i]['volumeInfo'].get('categories'),
                'rating' : answer['items'][i]['volumeInfo'].get('pageRating'),
                # 'thumbnail' : answer['items'][i]['volumeInfo'].get('imageLink').get('thumbnail'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks', {}).get('thumbnail', 'https://example.com/default-image.jpg'),
                'preview' : answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            contaxt = {
                'form' : form,
                'results' : result_list
            }
        return render(request, 'dashboard/books.html',contaxt)
    else:
        form = DashboardForm()

    contaxt = {'form' : form}
    return render(request, 'dashboard/books.html', contaxt) 


# Dictionary Section

def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"+text
        # url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+text
        r = requests.get(url)
        answer = r.json()
        try:
            phonetics = answer[0]['phonetics'][0]['text']
            audio = answer[0]['phonetics'][0]['audio']
            definition = answer[0]['meanings'][0]['definitions'][0]['definition']
            example = answer[0]['meanings'][0]['definitions'][0]['example']
            synonyms = answer[0]['meanings'][0]['definitions'][0]['synonyms']
            contaxt = {
                'form' : form,
                'input' : text,
                'phonetics' : phonetics,
                'audio' : audio,
                'definition' : definition,
                'example' : example,
                'synonyms' : synonyms
            }
        except:
            contaxt = {
                'form' : form,
                'input' : '',
            }
        return render(request, 'dashboard/dictionary.html', contaxt)
    else:
        form = DashboardForm()
        
    contaxt = {
        'form' : form
    }
    return render(request, 'dashboard/dictionary.html', contaxt)


# Wkipedia Section
def wiki(request):
    if request.method == 'POST':
        text = request.POST['text']
        form = DashboardForm(request.POST)
        search = wikipedia.page(text)
        context = {
            'form' : form,
            'title' : search.title,
            'link' : search.url,
            'details' : search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        contaxt = {
        'form' : form
        }
    return render(request, 'dashboard/wiki.html', contaxt)


# Conversion Section
def conversion(request):
    if request.method == 'POST':
        form = ConversionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form = ConversionLengthForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''
                if input_value and int(input_value) >= 0:
                    if first == 'yard' and second == 'foot':
                        answer = f'{input_value} yard = {int(input_value) * 3} foot'
                    elif first == 'foot' and second == 'yard':
                        answer = f'{input_value} foot = {int(input_value) / 3} yard'
                context['answer'] = answer

        elif request.POST['measurement'] == 'mass':
            measurement_form = ConversionMassForm(request.POST)
            context = {
                'form': form,
                'm_form': measurement_form,
                'input': True
            }
            if 'input' in request.POST:
                first = request.POST['measure1']
                second = request.POST['measure2']
                input_value = request.POST['input']
                answer = ''
                if input_value and int(input_value) >= 0:
                    if first == 'pound' and second == 'kilogram':
                        answer = f'{input_value} pound = {int(input_value) * 0.453592} kilogram'
                    elif first == 'kilogram' and second == 'pound':
                        answer = f'{input_value} kilogram = {int(input_value) * 2.20462} pound'
                context['answer'] = answer

        return render(request, 'dashboard/conversion.html', context)
    else:
        form = ConversionForm()
        context = {
            'form': form,
            'input': False
        }
        return render(request, 'dashboard/conversion.html', context)


# Registration sections
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    contaxt = {
        'form' : form
    }
    return render(request, 'dashboard/register.html', contaxt)

# Profile Section
def profile(request):
    homeworks = Homework.objects.filter(is_finished = False, user = request.user)
    todos = Todo.objects.filter(is_finished = False, user = request.user)
    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
    contaxt = {
        'homeworks' : homeworks,
        'todos' : todos,
        'homework_done' : homework_done,
        'todos_done' : todos_done
    }
    return render(request, 'dashboard/profile.html', contaxt)


def logout(request):
    return render(request, 'dashboard/logout.html')