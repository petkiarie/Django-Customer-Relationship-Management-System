from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, RecordForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Record

def home(request):

    return render(request, 'webapp/index.html')

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')
    context = {'form': form}

    return render(request, 'webapp/register.html', context)

def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    
    context = {'form': form}
    return render(request, 'webapp/my-login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect('my-login')

@login_required(login_url='my-login')
def dashboard(request):
    records = Record.objects.all()
    context = {'records': records}
    return render(request, 'webapp/dashboard.html', context)

# add a record
@login_required(login_url='my-login')
def create_record(request):
    form = RecordForm()

    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'webapp/create-record.html', context)

@login_required(login_url='my-login')
def update_record(request, pk):
   record = Record.objects.get(id=pk)
   form = RecordForm(instance=record)
   if request.method == 'POST':
       form = RecordForm(request.POST, instance=record)
       if form.is_valid():
           form.save()
           return redirect('record', pk=pk)
   context = {'form': form}
   return render(request, 'webapp/update-record.html', context)

@login_required(login_url='my-login')
def delete_record(request, pk):
    record = Record.objects.get(id=pk)
    record.delete()
    return redirect('dashboard')

@login_required(login_url='my-login')
def record_details(request, pk):
    record = get_object_or_404(Record, id=pk)
    context = {'record': record}
    return render(request, 'webapp/record-details.html', context)