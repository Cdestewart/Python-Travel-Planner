from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt

def index(request):
    try:
        request.session['user_id']
        return redirect('/travels')
    except:
        content = User.objects.all().values()
        return render(request, "first_app/index.html", {'content':content})

def new(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:   
        User.objects.create(fname = request.POST['fname'], lname = request.POST['lname'], email = request.POST['email'], password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        
        request.session['user_id'] = User.objects.get(email =request.POST['email']).id
        request.session['fname'] = User.objects.get(email =request.POST['email']).fname
        return redirect('/travels')

def login(request):
    errors = User.objects.existing(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    request.session['user_id'] = User.objects.get(email =request.POST['email']).id
    request.session['fname'] = User.objects.get(email =request.POST['email']).fname
    return redirect('/travels')


def dashboard(request):
    try:
        request.session['user_id']
        trips = Trip.objects.all().exclude(Attendee=request.session['user_id']).order_by('-created_at')
        attend = Trip.objects.all().filter(Attendee=request.session['user_id'])
        return render(request, "first_app/travels.html",{'trips' :trips, 'attend':attend})
    except:
        return redirect('/')

def details(request,num):
    try:
        request.session['user_id']
        trip = Trip.objects.get(id = num)
        attend = Trip.objects.get(id = num).Attendee.exclude(id = trip.creator.id).values()
        return render(request, "first_app/details.html", {'trip':trip, 'attend':attend})
    except:
        return redirect('/')

def addpage(request):
    try:
        request.session['user_id']
        return render(request, "first_app/add.html")
    except:
        return redirect('/')

def addtrip(request):
    errors = Trip.objects.trip(request.POST)
    if len(errors):
        for key, value in errors.items():
            print(value)
            messages.error(request, value)
        return redirect('/addtrip')
    Trip.objects.create(Destination = request.POST['Destination'], Description = request.POST['Description'], creator = User.objects.get(id=request.session['user_id']), travel_from = request.POST['from'], travel_to =  request.POST['to'])
    Trip.objects.last().Attendee.add(User.objects.get(id = request.session['user_id']))
    return redirect('/travels')

def subscribe(request,num):
    Trip.objects.get(id = num).Attendee.add(User.objects.get(id =request.session['user_id']))
    return redirect('/travels')

def delete(request,num):
    trip = Trip.objects.get(id = num)
    if(trip.creator.id == request.session['user_id']):
        trip.delete()
    return redirect('/travels')

def cancel(request,num):
    Trip.objects.get(id = num).Attendee.remove(User.objects.get(id = request.session['user_id']))
    return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/login')