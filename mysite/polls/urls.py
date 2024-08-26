from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "polls"

urlpatterns = [
    #======Index=============================
    path("", views.index, name="index"),
    #=====Forms==============================
    path("simplepurchase/", views.simple_purchase, name="simplepurchase"),
    #====Actions=============================
    path("do_nothing/", views.do_nothing, name="do_nothing"),
    path("modelform_to_model/", views.modelform_to_model, name="modelform_to_model"),
    #=====Submission Response=================
    path("thanks/", views.thanks, name="thanks"),
] + [
    path("purchase_contact/", views.purchase_contact, name="purchase_contact"),
    path("purchase_contact_get/", views.purchase_contact_get, name="purchase_contact_get"),
    path("purchase_items/<employee>/<dept>/", views.purchase_items, name="purchase_items"),
    path("purchase_save/", views.purchase_save, name="purchase_save")
] + [
    path("cart_contact/", views.cart_contact, name="cart_contact"),
    path("cart_contact_get/", views.cart_contact_get, name="cart_contact_get"),
    path("cart_items/<id>/", views.cart_items, name="cart_items"),
    path("cart_save/<id>/", views.cart_save, name="cart_save")
]

#A purchase has purchase_contact, purchase_contact_get, purchase_items, purchase_save, and thanks.