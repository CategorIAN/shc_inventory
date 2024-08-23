from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "polls"
urlpatterns = []

urlpatterns = [
    #======Index=============================
    path("", views.index, name="index"),
    #=====Forms==============================
    path("simplepurchase/", views.simple_purchase, name="simplepurchase"),
    path("purchase_initial/", views.purchase_initial, name="purchase_initial"),
    path("purchase_items/<employee>/<dept>/", views.purchase_items, name="purchase_items"),
    #====Actions=============================
    path("do_nothing/", views.do_nothing, name="do_nothing"),
    path("modelform_to_model/", views.modelform_to_model, name="modelform_to_model"),
    path("enter_initial/", views.enter_initial, name="enter_initial"),
    path("submit_purchase/<id>/", views.submit_purchase, name="submit_purchase"),
    #=====Submission Response=================
    path("thanks/", views.thanks, name="thanks"),
]