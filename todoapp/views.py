from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
         username = request.POST['username']
         email = request.POST['email']
         password = request.POST['password']
         confirm_password = request.POST['confirm_password'] 
         if password == confirm_password:
               if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return redirect('signup')
               elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('signup')
               else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    print('User Created')
                    return redirect('login')
         else:
               messages.info(request, 'Password not matching..')
               return redirect('signup')
    else:
         return render(request, 'signup.html')

def login(request):
     if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = auth.authenticate(username=username, password=password)

          if user is not None:
               auth.login(request, user)
               return redirect('task_list')
          else:
               messages.info(request, 'Invalid Credentials')
               return redirect('login')
     else:
          return render(request, 'login.html')
     
@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'add_task.html')

def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def delete_task(request, task_id):
    Task.objects.get(id=task_id).delete()
    return redirect('task_list')
