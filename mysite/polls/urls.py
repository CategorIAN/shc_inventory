from django.urls import path
from . import views

app_name = "polls"

urlpatterns = [
    path("", views.index, name="index"),
    path("thanks/", views.thanks, name="thanks"),
    path("cart_contact/", views.cart_contact, name="cart_contact"),
    path("cart_contact_get/", views.cart_contact_get, name="cart_contact_get"),
    path("cart_items/<id>/", views.cart_items, name="cart_items"),
    path("cart_save/<id>/", views.cart_save, name="cart_save"),
]