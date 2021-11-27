from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Person, PersonType, Restaurant, Contact, Delivery, Review, RestaurantDish, Address, Cuisine
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

import hashlib


def logout(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect("/login")


def index(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        cuisines_id = request.GET.get("cuisine")
        if cuisines_id:
            all_entries = Restaurant.objects.filter(cuisine__id=cuisines_id)
        else:
            all_entries = Restaurant.objects.all()
        cuisines = Cuisine.objects.all()
        
        return render(request, 'index.html', {"restaurants": all_entries, "cuisines":cuisines})


def login(request):
    if request.session.get('user_id'):
        return redirect("/")
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        try:
            person = authenticate(username=username, password=password)
            if person:
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
            new_user = Person(
                username=username,
                first_name=first_name,
                last_name=last_name,
                date_of_birth=date,
                person_type=PersonType.objects.get(type='User')
            )
            new_user.set_password(password)
            new_user.save()
            request.session['user_id'] = new_user.id
            return redirect('/')


def cart(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            dishes = []
            for rd_id in request.session.get('cart', []):
                dishes.append(RestaurantDish.objects.get(id=rd_id))
            return render(request, "cart.html", {"cart": dishes, "price": sum(map(lambda x: x.price, dishes))})
        except ObjectDoesNotExist:
            return redirect("/")


def add_cart(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.session.get('cart'):
        request.session['cart'] += [pk]
    else:
        request.session['cart'] = [pk]
    return redirect("/cart")


def restaurant_info(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            restaurant = Restaurant.objects.get(id=pk)
            rd = RestaurantDish.objects.get(restaurant=restaurant)
            reviews = Review.objects.filter(restaurant_dish=rd)
            return render(request, "restaurant_info.html", {"restaurant": restaurant, "reviews": reviews})
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


def edit_address(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")

    try:
        address = Address.objects.get(id=pk)
        person = Person.objects.get(
            id=request.session['user_id'], address=address)
    except ObjectDoesNotExist:
        return redirect("/")
    if request.method == 'GET':
        return render(request, "forms/address.html", {"address": address, "person": person})
    if request.method == 'POST':
        if request.POST.get("remove", ""):
            address.delete()
        if request.POST.get("edit", ""):
            address.city = request.POST.get("city", "")
            address.street = request.POST.get("street", "")
            address.zip = request.POST.get("zip", "")
            address.street_number = request.POST.get("street_number", "")
            address.save()
        if request.POST.get("add", ""):
            person.address.create(
                city=request.POST.get("city", ""),
                street=request.POST.get("street", ""),
                zip=request.POST.get("zip", ""),
                street_number=request.POST.get("street_number", ""),
            )
        return redirect("/user")


def show_reviews(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    if request.method == 'GET':
        try:
            restaurant_dish_id = request.GET.get("id")
            reviews = Review.objects.filter(
                restaurant_dish__id=restaurant_dish_id)
        except ObjectDoesNotExist:
            return redirect("/")
        return render(request, "reviews.html", {"reviews": reviews})
    return redirect("/")


def edit_review(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")

    try:
        person = Person.objects.get(id=request.session['user_id'])
        rd = RestaurantDish.objects.get(id=pk)
        reviews = Review.objects.filter(restaurant_dish=rd, reviewer=person)
        review = {}
        if reviews:
            review = reviews[0]
    except ObjectDoesNotExist:
        return redirect("/")

    if request.method == 'GET':
        return render(request, "forms/review.html", {"review": review, "person": person, "restaurat_dish": rd})
    if request.method == 'POST':
        if request.POST.get("remove", ""):
            review.delete()
        if request.POST.get("edit", ""):
            review.rating = request.POST.get("rating", "")
            review.text = request.POST.get("text", "")
            review.save()
        if request.POST.get("add", ""):
            Review.objects.create(
                reviewer=person,
                rating=request.POST.get("rating", ""),
                text=request.POST.get("text", ""),
                restaurant_dish=rd,
            )
        return redirect("/")


def edit_contact(request, pk):
    if not request.session.get('user_id'):
        return redirect("/login")

    try:
        person = Person.objects.get(id=request.session['user_id'])
        contact = Contact.objects.get(id=pk, person=person)
    except ObjectDoesNotExist:
        return redirect("/")

    if request.method == 'GET':
        return render(request, "forms/contact.html", {"contact": contact, "person": person})
    if request.method == 'POST':
        if request.POST.get("remove", ""):
            contact.delete()
        if request.POST.get("edit", ""):
            contact.type = request.POST.get("type", "")
            contact.value = request.POST.get("value", "")
            contact.save()
        if request.POST.get("add", ""):
            Contact.objects.create(
                person=person,
                type=request.POST.get("type", ""),
                value=request.POST.get("value", ""),
            )
        return redirect("/user")
