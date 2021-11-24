from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('user', views.info),
    path('deliveries', views.delivery_info),
    path('cart', views.cart),
    path('reviews', views.show_reviews),
    path('add_cart/<int:pk>', views.add_cart),
    path('user/<int:pk>', views.user_info),
    path('restaurant/<int:pk>', views.restaurant_info),
    path('edit/review/<int:pk>', views.edit_review),
    path('edit/address/<int:pk>', views.edit_address),
    path('edit/contact/<int:pk>', views.edit_contact),
]
