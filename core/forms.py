from django import forms
from django.forms import ModelForm
from .models import *

class SolicitudProductoForm(forms.ModelForm):
    class Meta:
        model = SolicitudProducto
        fields = ['quantity']
        labels = {
            'quantity': 'Cantidad',
        }
        widgets = {
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'id': 'idCantidad', 'min': '1'}),
        }