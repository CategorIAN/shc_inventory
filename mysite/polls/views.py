from django.http import HttpResponseRedirect
from .models import (SimplePurchaseForm, PurchaseForm, Employee, Department, Item_Purchase, Purchase,
                     Item_Purchase_Form, getItemPurchaseForm, getCart, Cart, Cart_Form, checkout_cart)
from django.shortcuts import render
from django.forms import modelformset_factory

def index(request):
    return render(request, "polls/index.html", {})

def thanks(request):
    return render(request, "polls/thanks.html", {})

def do_nothing(request):
    return HttpResponseRedirect("/polls/thanks")
#==================================================================================================================
def simple_purchase(request):
    return render(request, "polls/simplepurchase.html", {"form": SimplePurchaseForm()})

def modelform_to_model(request):
    SimplePurchaseForm(request.POST).save()
    return HttpResponseRedirect("/polls/thanks")
#==================================================================================================================
def purchase_contact(request):
    return render(request, "polls/purchase_contact.html", {"form": PurchaseForm()})

def purchase_contact_get(request):
    initial = PurchaseForm(request.POST)
    employee, dept = initial.data['employee'], initial.data['dept']
    return HttpResponseRedirect("/polls/purchase_items/{}/{}".format(employee, dept))

def purchase_items(request, employee, dept):
    employee = Employee.objects.get(id=employee)
    dept = Department.objects.get(cost_center=dept)
    purchase = Purchase(employee=employee, dept=dept)
    purchase.save()
    form = getItemPurchaseForm(purchase.pk)
    IPFormSet = modelformset_factory(Item_Purchase, form=form, min_num=2)
    formset = IPFormSet(queryset=Item_Purchase.objects.none())
    context = {"employee": employee, "dept": dept, "formset": formset}
    return render(request, "polls/purchase_items.html", context)

def purchase_save(request):
    RIPFormSet = modelformset_factory(Item_Purchase, form=Item_Purchase_Form)
    formset = RIPFormSet(request.POST)
    formset.save()
    return HttpResponseRedirect("/polls/thanks")
#==================================================================================================================
def cart_contact(request):
    Cart.objects.all().delete()
    return render(request, "polls/cart_contact.html", {"form": PurchaseForm()})

def cart_contact_get(request):
    initial = PurchaseForm(request.POST)
    employee, dept = initial.data['employee'], initial.data['dept']
    employee_obj = Employee.objects.get(id=employee)
    dept_obj = Department.objects.get(cost_center=dept)
    purchase = Purchase(employee=employee_obj, dept=dept_obj)
    purchase.save()
    return HttpResponseRedirect("/polls/cart_items/{}".format(purchase.pk))

def cart_items(request, id):
    purchase = Purchase.objects.get(pk=id)
    Enter_Class = modelformset_factory(Cart, form=getCart(id, edit=True), max_num=1)
    Cart_Class = modelformset_factory(Cart, form=getCart(id, edit=False), max_num=0)
    add_item = Enter_Class(queryset=Item_Purchase.objects.none(), prefix="add_item")
    cart = Cart_Class(prefix="cart")
    context = {"purchase": purchase, "formset_1": add_item, "formset_2": cart}
    return render(request, "polls/cart_items.html", context)

def cart_save(request, id):
    CartFormSet = modelformset_factory(Cart, form=Cart_Form)
    if "add_item" in request.POST:
        to_add = CartFormSet(request.POST, prefix="add_item")
        to_add.save()
        return HttpResponseRedirect("/polls/cart_items/{}".format(id))
    elif "delete" in request.POST:
        index = int(request.POST["delete"].strip("Delete Item "))
        cart_item = Cart.objects.all()[index - 1]
        cart_item.delete()
        return HttpResponseRedirect("/polls/cart_items/{}".format(id))
    elif "checkout" in request.POST:
        checkout_cart()
        return HttpResponseRedirect("/polls/thanks")
#==================================================================================================================

