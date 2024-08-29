from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import render
from django.forms import modelformset_factory
from django.db.models import F, Sum

def index(request):
    return render(request, "polls/index.html", {})

def thanks(request):
    return render(request, "polls/thanks.html", {})

def cart_contact(request):
    return render(request, "polls/cart_contact.html", {"form": PurchaseForm()})

def cart_contact_get(request):
    initial = PurchaseForm(request.POST)
    employee, dept = initial.data['employee'], initial.data['dept']
    purchase = Purchase(employee=Employee.objects.get(id=employee), dept=Department.objects.get(cost_center=dept))
    purchase.save()
    return HttpResponseRedirect("/polls/cart_items/{}".format(purchase.pk))

def cart_items(request, id):
    purchase = Purchase.objects.get(pk=id)
    Enter_Class = modelformset_factory(Cart, form=getCart(id, hide_item=False), max_num=1)
    Cart_Class = modelformset_factory(Cart, form=getCart(id, hide_item=True), max_num=0)
    add_item_formset = Enter_Class(queryset=Cart.objects.none(), prefix="add_item")
    current_cart = Cart.objects.filter(purchase=id)
    cart_formset = Cart_Class(queryset=current_cart, prefix="cart")
    total = current_cart.annotate(price = F("item__cost") * F("quantity")).aggregate(Sum("price"))["price__sum"]
    cart_items_forms = zip([cart_object.item.name for cart_object in current_cart], [form for form in cart_formset])
    context = {"purchase": purchase, "add_item_fs": add_item_formset, "cart_fs": cart_formset,
               "total": money_string(total), "cart": cart_items_forms}
    return render(request, "polls/cart_items.html", context)

def cart_save(request, id):
    if "add_item" in request.POST:
        modelformset_factory(Cart, form=Cart_Form)(request.POST, prefix="add_item").save()
        return HttpResponseRedirect("/polls/cart_items/{}".format(id))
    elif "delete" in request.POST:
        Cart.objects.filter(purchase=id)[int(request.POST["delete"].strip("Delete Item ")) - 1].delete()
        return HttpResponseRedirect("/polls/cart_items/{}".format(id))
    elif "checkout" in request.POST:
        modelformset_factory(Cart, form=Cart_Form)(request.POST, prefix="cart").save()
        checkout_cart(id)
        return HttpResponseRedirect("/polls/thanks")
    elif "scan_barcode" in request.POST:
        Cart(purchase_id=id, item_id=int(request.POST["barcode"]), quantity=1).save()
        return HttpResponseRedirect("/polls/cart_items/{}".format(id))
