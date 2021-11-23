from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('user', views.info),
    path('deliveries', views.delivery_info),
    path('user/<int:pk>', views.user_info),
    path('restaurant/<int:pk>', views.restaurant_info),
    path('edit/address/<int:pk>', views.edit_address),
    path('edit/contact/<int:pk>', views.edit_contact),
]
