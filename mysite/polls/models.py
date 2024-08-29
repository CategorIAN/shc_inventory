from django.db import models
from django.forms import ModelForm
from django import forms
from django.db.models.functions import Now

class Department(models.Model):
    cost_center = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Item(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    room = models.CharField(max_length=100)

    def __str__(self):
        return "{} (${})".format(self.name, self.cost)

class Employee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
#=========================================================================================
class Purchase(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

class Item_Purchase(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

class Cart(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
#===========================================================================================
class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ["employee", "dept"]

class Cart_Form(ModelForm):
    class Meta:
        model = Cart
        fields = ["purchase", "item", "quantity"]
#=======================================Helper Functions====================================================
def getCart(purchase_id, hide_item):
    class X(Cart_Form):
        def __init__(self, *args, **kwargs):
            initial = kwargs.get('initial', {})
            initial["purchase"] = Purchase.objects.get(pk=purchase_id)
            kwargs['initial'] = initial
            super().__init__(*args, **kwargs)
            self.fields["purchase"].widget = forms.HiddenInput()
            if hide_item:
                self.fields["item"].widget = forms.HiddenInput()
    return X

def checkout_cart(id):
    cart = Cart.objects.filter(purchase=id)
    for cart_item in cart:
        Item_Purchase(purchase=cart_item.purchase, item=cart_item.item, quantity=cart_item.quantity).save()
    cart.delete()

def money_string(value):
    return "$0.00" if value is None else f"${value:.2f}"


