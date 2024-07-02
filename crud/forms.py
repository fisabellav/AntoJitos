from django import forms
from django.forms import ModelForm
from .models import *

class ProductForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'resize: none; height:80px'})
    )
    flavor = forms.ModelMultipleChoiceField(
        queryset=Flavor.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True  # Hace que el campo sea requerido
    )

    class Meta:
        model = Product
        fields = ['product', 'description', 'image', 'flavor', 'category']
        widgets = {
            'product': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }