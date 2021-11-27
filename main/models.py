from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, date_of_birth=None, last_name=None, person_type=None, first_name=None):
        user = self.model(
            username=username,
            date_of_birth=date_of_birth,
            last_name=last_name,
            first_name=first_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, date_of_birth=None, last_name=None, first_name=None, email=None):
        user = self.create_user(
            username=username,
            password=password,
            date_of_birth=date_of_birth,
            last_name=last_name,
            first_name=first_name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


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


class Person(AbstractBaseUser):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45, unique=True)
    date_of_birth = models.DateField()
    person_type = models.ForeignKey(PersonType, on_delete=models.CASCADE, blank=True, null=True)
    address = models.ManyToManyField(Address)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['date_of_birth', 'last_name', 'first_name']
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


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
