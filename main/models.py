from django.db import models
from django.contrib.auth.models import User


class PersonType(models.Model):
    type = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.type}"


class Address(models.Model):
    city = models.CharField(max_length=45)
    street = models.CharField(max_length=45)
    street_number = models.IntegerField()
    zip = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.city} {self.street} {self.street_number}"


class Person(models.Model):
    USER_TYPES = (
        ('user', 'USER'),
        ('admin', 'ADMIN'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    type = models.CharField(max_length=50, choices=USER_TYPES)
    address = models.ManyToManyField(Address)

    def __str__(self):
        return f"{self.type} - {self.user.username}"


# TODO: Add list of params to the type
class Contact(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    type = models.CharField(max_length=45)
    value = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.person} {self.type}:{self.value}"


class Car(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    plate = models.CharField(max_length=45)
    type = models.CharField(max_length=45)
    brand = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.person} {self.plate}"


class Shift(models.Model):
    drivers = models.ManyToManyField(Person)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class Cuisine(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name}"


class Dish(models.Model):
    name = models.CharField(max_length=45)

    def __str__(self):
        return f"{self.name}"


class Restaurant(models.Model):
    name = models.CharField(max_length=45)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    dishes = models.ManyToManyField(Dish, through='RestaurantDish')
    cuisine = models.ForeignKey(Cuisine, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class RestaurantDish(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="restaurant_dish")
    price = models.IntegerField()
    description = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.restaurant} - {self.dish} - {self.price}"


class Delivery(models.Model):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        Person, on_delete=models.CASCADE, related_name='driver')
    arival = models.DateTimeField(blank=True, auto_now_add=True)
    delivery_fee = models.IntegerField(blank=True, default=0)
    dishes = models.ManyToManyField(RestaurantDish, through='DeliveryDish')

    def __str__(self):
        return f"Order: {self.person} - Driver: {self.driver} - {self.arival}"


class DeliveryDish(models.Model):
    dish = models.ForeignKey(RestaurantDish, on_delete=models.CASCADE)
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="delivery_dish")
    requirements = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.dish} | {self.delivery} | {self.requirements}"


class Review(models.Model):
    reviewer = models.ForeignKey(
        Person, on_delete=models.CASCADE)
    driver = models.ForeignKey(
        Person, blank=True, null=True, on_delete=models.CASCADE, related_name='review_driver')
    restaurant_dish = models.ForeignKey(
        RestaurantDish, blank=True, null=True, on_delete=models.CASCADE)
    rating = models.SmallIntegerField()
    text = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.reviewer} - {self.rating} - {self.text}"
