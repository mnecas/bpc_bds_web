from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.models import Person, PersonType, Restaurant, Contact, Delivery, Review, RestaurantDish, Address, Cuisine
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db import connection
import hashlib
import logging
import bcrypt


logger = logging.getLogger(__name__)


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

        return render(request, 'index.html', {"restaurants": all_entries, "cuisines": cuisines})


def login(request):
    if request.session.get('user_id'):
        return redirect("/")
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        try:
            user = Person.objects.get(username=username)
            if bcrypt.checkpw(password.encode('utf-8'), user.password):
                request.session['user_id'] = user.id
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
        if not (username and password and first_name and last_name and date):
            return redirect('/register')
        try:
            # Check if the person exists if it doe return error
            Person.objects.get(username=username)
            return render(request, 'register.html', {'user_exists': True})
        except ObjectDoesNotExist:
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            with transaction.atomic():
                new_user = Person.objects.create(
                    date_of_birth=date,
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    password=password_hash,
                    type='user'
                )
            request.session['user_id'] = new_user.id
            return redirect('/')


def test_sql_injection(request):
    if request.method == 'GET':
        persons = []
    elif request.method == 'POST':
        # SQL INJECTIONS
        # \' OR 1=1;--
        # \';DELETE FROM main_custom_drop_table;--

        # Django query
        #persons = Person.objects.filter(username=request.POST.get("username", ""))

        # SQL raw without prepare statement
        query = "SELECT * FROM main_person WHERE 'main_person'.'username' = \'" + \
            request.POST.get("username", "")+"\'"
        persons = Person.objects.raw(query)

        # SQL raw with prepare statement
        #query = "SELECT * FROM main_person WHERE 'main_person'.'username' = %s"
        #persons = Person.objects.raw(query, [request.POST.get("username", "")])
        print(query)
        print(persons)
        print(connection.queries)
    return render(request, "users.html", {"persons": persons})


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
            if person.type == 'user':
                reviews = Review.objects.filter(reviewer=person)
            elif person.type == 'driver':
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
        return redirect("/user")


def add_address(request):
    if not request.session.get('user_id'):
        return redirect("/login")

    try:
        person = Person.objects.get(id=request.session['user_id'])
    except ObjectDoesNotExist:
        return redirect("/")
    if request.method == 'GET':
        return render(request, "forms/address.html", {"person": person})
    if request.method == 'POST':
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


def add_contact(request):
    if not request.session.get('user_id'):
        return redirect("/login")
    try:
        person = Person.objects.get(id=request.session['user_id'])
    except ObjectDoesNotExist:
        return redirect("/")

    if request.method == 'GET':
        return render(request, "forms/contact.html", {"person": person})
    if request.method == 'POST':
        Contact.objects.create(
            person=person,
            type=request.POST.get("type", ""),
            value=request.POST.get("value", ""),
        )
        return redirect("/user")


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
        return redirect("/user")
