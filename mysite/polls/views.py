from django.http import HttpResponseRedirect
from .models import (SimplePurchaseForm, PurchaseForm, Employee, Department, Item_Purchase, Purchase, Item_Purchase_Form,
                     getItemPurchaseForm)
from django.shortcuts import render
from django.forms import modelformset_factory

def index(request):
    return render(request, "polls/index.html", {})

def thanks(request):
    return render(request, "polls/thanks.html", {})

def do_nothing(request):
    return HttpResponseRedirect("/polls/thanks")

def simple_purchase(request):
    return render(request, "polls/simplepurchase.html", {"form": SimplePurchaseForm()})

def modelform_to_model(request):
    SimplePurchaseForm(request.POST).save()
    return HttpResponseRedirect("/polls/thanks")

def purchase_initial(request):
    return render(request, "polls/purchase_initial.html", {"form": PurchaseForm()})

def enter_initial(request):
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
'''
def submit_purchase(request, id):
    form = getItemPurchaseForm(id)
    RIPFormSet = modelformset_factory(Item_Purchase, form=form)
    formset = RIPFormSet(request.POST)
    formset.save()
    return HttpResponseRedirect("/polls/thanks")
'''

def submit_purchase(request):
    IPFormSet = modelformset_factory(Item_Purchase, form=Item_Purchase_Form)
    formset = IPFormSet(request.POST)
    formset.save()
    return HttpResponseRedirect("/polls/thanks")


