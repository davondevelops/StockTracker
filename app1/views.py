from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import requests
import datetime
# Create your views here.


def index(request):
    request.session['id']=0
    return render(request, 'index.html')
def login(request):
    request.session['id']=0
    return render(request, 'login.html')
def register(request):
    request.session['id']=0
    return render(request, 'register.html')
def create(request):
    errors = User.objects.registration_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/register')
    x=request.POST
    hashedpassword= bcrypt.hashpw(x['pw'].encode(), bcrypt.gensalt(rounds=10)).decode()
    newUser=User.objects.create(first_name=x['fname'], last_name=x['lname'], email= x['email'],  password= hashedpassword)
    request.session['id']=newUser.id
    return redirect('/homepage')
def validate(request):
    x=request.POST
    errors = User.objects.login_validator(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    user= User.objects.filter(email=x['email'])
    request.session['id']=user[0].id
    return redirect('/homepage')
def homepage(request):
    if request.session['id']==0 or request.session['id']==None:
        return redirect('/login')
    x= request.session['id']
    context ={
        'loggedin': User.objects.get(id=x),
        'Current_date':datetime.datetime.today().strftime('%m/%d/%Y %H:%M:%S')
    }
    return render(request, 'homepage.html', context)
def logout(request):
    request.session['id']=0
    return redirect('/login')
def editAccount(request):
    if request.session['id']==0:
        return redirect('/login')
    x= request.session['id']
    context ={
        'loggedin': User.objects.get(id=x)
    }
    return render(request, 'editAccount.html', context)
def addStockStats(request):
    x= request.session['id']
    context ={
        'loggedin': User.objects.get(id=x)
    }
    return render(request,'stockTrackerForm.html', context)
def addtoVault(request):
    return render(request, 'addVault.html')
def comparetoVault(request):
    return render(request, 'comparetoVault.html')
def performance(request):
    return render(request, 'performance.html')