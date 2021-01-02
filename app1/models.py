from django.db import models
from datetime import date
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
    
    
class Stock(models.Model):
    ticker=models.CharField(max_length=5)
    
class Watchlist(models.Model):
    name=models.CharField(max_length=55)
    user= models.ForeignKey(User, related_name="watchlist", on_delete= models.CASCADE)
    
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StockHistory(models.Model):
    ticker= models.CharField(max_length=5)
    entry=models.DecimalField(decimal_places=2, max_digits=7)
    exit=models.DecimalField(decimal_places=2, max_digits=7)
    position_size=models.DecimalField(decimal_places=2, max_digits=7)
    is_buy=models.BooleanField()
    trade_pattern=models.CharField(max_length=55)
    sector=models.CharField(max_length=55)
    dateOfTrade=models.DateField()
    desc= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

class vault(models.Model):
    ticker= models.CharField(max_length=5)
    sector=models.CharField(max_length=55)
    open=models.DecimalField(decimal_places=2,max_digits=7)
    high=models.DecimalField(decimal_places=2,max_digits=7)
    low=models.DecimalField(decimal_places=2,max_digits=7)
    close=models.DecimalField(decimal_places=2,max_digits=7)
    previous_close=models.DecimalField(decimal_places=2,max_digits=7)
    volume=models.IntegerField()
    float=models.IntegerField()
    catalyst=models.CharField(max_length=55)
    lookupdate=models.DateField()
    year_high=models.DecimalField(decimal_places=2,max_digits=7)
    year_low=models.DecimalField(decimal_places=2,max_digits=7)
    market_cap=models.DecimalField(decimal_places=2,max_digits=20)
    created_at= models.DateTimeField(auto_now_add=True)
    