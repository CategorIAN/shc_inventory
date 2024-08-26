from django.http import HttpResponseRedirect
from .models import (SimplePurchaseForm, PurchaseForm, Employee, Department, Item_Purchase, Purchase,
                     Item_Purchase_Form, getItemPurchaseForm)
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
    return render(request, "polls/cart_contact.html", {"form": PurchaseForm()})

def cart_contact_get(request):
    initial = PurchaseForm(request.POST)
    employee, dept = initial.data['employee'], initial.data['dept']
    return HttpResponseRedirect("/polls/cart_items/{}/{}".format(employee, dept))

def cart_items(request, employee, dept):
    employee_obj = Employee.objects.get(id=employee)
    dept_obj = Department.objects.get(cost_center=dept)
    purchase = Purchase(employee=employee_obj, dept=dept_obj)
    purchase.save()
    form = getItemPurchaseForm(purchase.pk)
    IPFormSet = modelformset_factory(Item_Purchase, form=form, max_num=2)
    formset_1 = IPFormSet(queryset=Item_Purchase.objects.none(), prefix="formset1")
    formset_2 = IPFormSet(queryset=Item_Purchase.objects.none(), prefix="formset2")
    context = {"employee": employee, "dept": dept, "formset_1": formset_1, "formset_2": formset_2}
    return render(request, "polls/results.html", context)

def cart_save(request, employee, dept):
    RIPFormSet = modelformset_factory(Item_Purchase, form=Item_Purchase_Form)
    if "add_item" in request.POST:
        formset_1 = RIPFormSet(request.POST, prefix="formset1")
        formset_2 = RIPFormSet(request.POST, prefix="formset2")
        current_cart = list(formset_1) + list(formset_2)
        context = {"employee": employee, "dept": dept, "formset_1": formset_1,
                   "formset_2": current_cart}
        return render(request, "polls/cart_items.html", context)
    elif "checkout" in request.POST:
        formset = RIPFormSet(request.POST, prefix="formset2")
        formset.save()
    return HttpResponseRedirect("/polls/thanks")
#==================================================================================================================

