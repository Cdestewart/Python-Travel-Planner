from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import datetime
import bcrypt
class UserValidator(models.Manager):
    def validator(self, postData):
        errors ={}
        if len(postData['fname'])<2:
            errors['fname'] = "First name should be greater than 2 characters"
        if len(postData['lname'])<2:
            errors['lname'] = "Last name should be greater than 2 characters"
        for a in postData['fname']:
            if(a.isdigit()):
                errors['fname'] = "First name cannot have a number"
        for a in postData['lname']:
            if(a.isdigit()):
                errors['lname'] = "Last name cannot have a number"
        atsign = 0
        emailvalid = 0
        for i in postData['email']:
            if(i== '@'):
                atsign += 1
            if(atsign == 1 and i =='.'):
                emailvalid =1
        if(emailvalid != 1):
            errors['email'] = "Not a valid email"
        try:
            User.objects.get(email =postData['email'])
            errors['email'] = "Email already in use, please try logging in"
        except:
            pass
        if(len(postData['password']) <8):
            errors['password'] = "Password must be 8 letters or longer"
        if(postData['pconf'] != postData['password']):
            errors['pconf'] = "Passwords do not match"
        return errors
    def existing(self, postData):
        errors = {}
        try:
            user = User.objects.get(email = postData['email'])                
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()): 
                errors['password'] = "Incorrect password"
        except:
            errors['user'] = "Not a valid username"
        return errors


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length= 255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserValidator()

class TripValidator(models.Manager):
    def trip(self, postData):
        errors = {}
        if len(postData['Destination'])<1:
            errors['destination'] = "Trip must have a destination"
        if len(postData['Description'])<1:
            errors['description'] = "Trip must have a description"
        if postData['from']> postData['to']:
            errors['dates'] = "Trip must start before it ends"
        if len(postData['to']) <1:
            errors['to'] = "Trip must have an end date"
        if len(postData['from']) <1:
            errors['to'] = "Trip must have a start date"
        if (len(postData['from']) >1):
            if len(postData['to'])>1:
                tyear = datetime.now().year
                tmonth = datetime.now().month
                if tmonth <10:
                    tmonth = '0'+str(tmonth)
                tday = datetime.now().day
                today = str(tyear)+'-'+str(tmonth)+'-'+str(tday)
                if datetime.strptime(today, "%Y-%m-%d")> datetime.strptime(postData['from'], "%Y-%m-%d"):
                    errors['date'] = "Trip cannot start in the past"
        return errors

class Trip(models.Model):
    Destination = models.CharField(max_length = 255)
    Description = models.TextField(max_length = 1000, default ="")
    Attendee = models.ManyToManyField(User, related_name = "trip_id")
    creator = models.ForeignKey(User, related_name = "user_id", on_delete=models.CASCADE)
    travel_from = models.DateTimeField()
    travel_to = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripValidator()

