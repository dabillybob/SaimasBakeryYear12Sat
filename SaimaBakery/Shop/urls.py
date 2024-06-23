from django.urls import path
from . import views

urlpatterns = [
    path('', views.Shop, name="Shop"),
    path('Cart/', views.Cart, name='Cart'),
    path('Checkout/', views.Checkout, name='Checkout')
]