from django.db import models
from datetime import date,timedelta, datetime
from django.contrib.postgres.fields import ArrayField
import re

from django.db.models.fields import CharField
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        
        today = date.today()
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        
        
        if postData['fname']=='' :
            errors['fname']= "You have to have a first name!"
        if postData['lname']=='':
            errors['lname']= "Please enter a last name!"
        if postData['email']=='':
            errors['email']= "Please enter an email"
        elif not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        elif len(User.objects.filter(email=postData['email']))>0:
            errors['email'] = "Email already register. Try signing in."
        if postData['pw']=='':
            errors['pw']="You need to have a password!"
        elif postData['pw']!=postData['cpw']:
            errors['pw']="Passwords don't match!"
        return errors   
    
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        user= User.objects.filter(email=postData['email'])
        if len(user)== 0:
            errors['email'] = "Can't find user with that email. Try signing up."
        elif not bcrypt.checkpw(postData['pw'].encode(),user[0].password.encode()):
            errors['invalid']= 'Invalid login Information'
        return errors
    
    def update_validator(self, postData, user):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if postData['fname']=='' :
            errors['fname']= "You have to have a first name!"
        if postData['lname']=='':
            errors['lname']= "Please enter a last name!"
        if postData['email']=='':
            errors['email']= "Please enter an email"
        elif not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        elif postData['email']!=user.email:
            if len(User.objects.filter(email=postData['email']))>0:
                errors['email'] = "Email already register to another account"
        return errors
    def quote_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['author'])<3 :
            errors['author']= "Author name must have more than 3 characters!"
        if len(postData['quote'])<10:
            errors['quote']= "Quote must be at least 10 character!"
        return errors
        
class User(models.Model):
    first_name= models.CharField(max_length=45)
    last_name= models.CharField(max_length=45)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    favorite_sector=models.CharField(max_length=30, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()
    def __str__(self):
        return f"<User object: {self.first_name} ({self.id})>"

class Watchlist(models.Model):
    name=models.CharField(max_length=55)
    user= models.ForeignKey(User, related_name="watchlist", on_delete= models.CASCADE)
    date= models.CharField(max_length=20, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class StockWatchlist(models.Model):
    ticker=models.CharField(max_length=5)
    desc=models.TextField()
    watchlist= models.ForeignKey(Watchlist, related_name="stocks", on_delete= models.CASCADE)
    category= models.CharField(max_length=20)
    catalyst=models.CharField(max_length=45)
    created_at=models.DateTimeField(auto_now_add=True)


class stockVaultManager(models.Manager):
    def addToVault(self, postData):
        errors={}
        if postData['stock_ticker']=='' :
            errors['stock_ticker']= "Well you need a stock!"
        return errors
class StockHistoryManager(models.Manager):
    def validateForm(self,postData):
        errors={}
        if postData['entry']=='':
            errors['entry']='Please insert a value for entry'
        if postData['exit']=='':
            errors['exit']='Please insert a value for exit'
        if postData['position_size']=='':
            errors['position_size']='Please insert a value for position size'
        if postData['pattern']=='':
            errors['pattern']='Please insert the pattern type. Insert None if N/A'
        if postData['date']=='':
            errors['date']='Please insert a date'
        # elif postData['date']>datetime.today():
        #     errors['date']="You can't trade in the future"
        if postData['sector']=='':
            errors['sector']='Please insert the sector'
        return errors



class StockHistory(models.Model):
    ticker= models.CharField(max_length=5)
    entry=models.DecimalField(decimal_places=3, max_digits=7)
    exit=models.DecimalField(decimal_places=3, max_digits=7)
    fee=models.DecimalField(decimal_places=2, max_digits=7,default=0)
    position_size=models.DecimalField(decimal_places=2, max_digits=7)
    buy_or_short=models.CharField(max_length=5)
    trade_pattern=models.CharField(max_length=55)
    sector=models.CharField(max_length=55)
    dateOfTrade=models.DateField()
    desc= models.TextField(null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    objects=StockHistoryManager()
    user= models.ForeignKey(User, related_name="stockHistory", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class vault(models.Model):
    user= models.ForeignKey(User, related_name="uservault", on_delete= models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)

class stockVault(models.Model):
    vault= models.ForeignKey(vault, related_name="stockVault", on_delete= models.CASCADE, default=0)
    ticker= models.CharField(max_length=5)
    sector=models.CharField(max_length=55)
    industry=models.CharField(max_length=100)
    open=models.DecimalField(decimal_places=2,max_digits=7)
    high=models.DecimalField(decimal_places=2,max_digits=7)
    low=models.DecimalField(decimal_places=2,max_digits=7)
    close=models.DecimalField(decimal_places=2,max_digits=7)
    previous_close=models.DecimalField(decimal_places=2,max_digits=7)
    volume=models.IntegerField()
    float=models.IntegerField()
    exchange=models.CharField(max_length=25)
    pattern=models.CharField(max_length=55, default='None')
    year_high=models.DecimalField(decimal_places=2,max_digits=7)
    year_low=models.DecimalField(decimal_places=2,max_digits=7)
    market_cap=models.DecimalField(decimal_places=2,max_digits=20)
    daychart=ArrayField(ArrayField(models.DecimalField(decimal_places=2,max_digits=20)))
    type=CharField(max_length=10, default=[])
    created_at= models.DateTimeField(auto_now_add=True)
    objects=stockVaultManager()
    
        
    
    
    