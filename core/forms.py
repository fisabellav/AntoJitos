from django import forms
from django.forms import ModelForm
from .models import *


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['quantity']  # Dejamos solo 'quantity' ya que 'order' y 'product' se manejarán de manera diferente
        labels = {
            'quantity': 'Cantidad',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control cantidad', 'id': 'idCantidad', 'min': '1'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['total', 'status']  # 'quantity' se manejará de manera diferente
        labels = {
            'total': 'Total',
            'status': 'Estado',
        }
        widgets = {
            'total': forms.NumberInput(attrs={'class': 'form-control', 'id': 'idTotal'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'idStatus'}),
        }