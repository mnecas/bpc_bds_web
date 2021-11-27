from django.contrib import admin

from .models import *

admin.site.register(PersonType)
admin.site.register(Person)
admin.site.register(Contact)
admin.site.register(Car)
admin.site.register(Shift)
admin.site.register(Address)
admin.site.register(Cuisine)
admin.site.register(Dish)
admin.site.register(Restaurant)
admin.site.register(RestaurantDish)
admin.site.register(Delivery)
admin.site.register(DeliveryDish)
admin.site.register(Review)
admin.site.register(CustomDropTable)
