from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Person, PersonType, Restaurant, Contact, Delivery, Review, RestaurantDish
from django.core.exceptions import ObjectDoesNotExist

import hashlib


def logout(request):
    del request.session['user_id']
    return redirect("/login")


def index(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        all_entries = Restaurant.objects.all()
        return render(request, 'index.html', {"restaurants": all_entries})


def login(request):
    if request.session.get('user_id'):
        return redirect("/")
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        try:
            person = Person.objects.get(username=username)
            if person.password == hashlib.sha224(password.encode()).hexdigest():
                request.session['user_id'] = person.id
                return redirect("/")
            else:
                return render(request, "login.html", {"wrong": True})
        except ObjectDoesNotExist:
            return render(request, "login.html", {"wrong": True})
    return render(request, 'login.html')


def register(request):
    if request.session.get('user_id'):
        return redirect("/")
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        date = request.POST.get("birthday", "")
        try:
            # Check if the person exists if it doe return error
            Person.objects.get(username=username)
            return render(request, 'register.html', {'user_exists': True})
        except ObjectDoesNotExist:
            new_user = Person.objects.create(
                username=username,
                password=hashlib.sha224(password.encode()).hexdigest(),
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date,
                person_type=PersonType.objects.get(type='User')
            )
            request.session['user_id'] = new_user.id
            return redirect('/')


def restaurant_info(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            restaurant = Restaurant.objects.get(id=pk)
            rd = RestaurantDish.objects.get(restaurant=restaurant)
            reviews = Review.objects.filter(restaurant_dish=rd)
            return render(request, "restaurant_info.html", {"restaurant": restaurant})
        except ObjectDoesNotExist:
            return redirect("/")


def user_info(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            person = Person.objects.get(id=pk)
            contacts = Contact.objects.filter(person=person)
            reviews = None
            if person.person_type.type == 'User':
                reviews = Review.objects.filter(reviewer=person)
            elif person.person_type.type == 'Driver':
                reviews = Review.objects.filter(driver=person)
            return render(request, "user_info.html", {"person": person, "contacts": contacts, "reviews": reviews})
        except ObjectDoesNotExist:
            return redirect("/")


def info(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            person = Person.objects.get(id=request.session['user_id'])
            contacts = Contact.objects.filter(person=person)
            reviews = Review.objects.filter(reviewer=person)
            return render(request, "info.html", {"person": person, "contacts": contacts, "reviews": reviews})
        except ObjectDoesNotExist:
            return redirect("/")


def delivery_info(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            person = Person.objects.get(id=request.session['user_id'])
            deliveries = Delivery.objects.filter(person=person)
            return render(request, "delivery_info.html", {"person": person, "deliveries": deliveries})
        except ObjectDoesNotExist:
            return redirect("/")
