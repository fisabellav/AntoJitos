from django import forms
from django.forms import ModelForm
from .models import *

class UserForm(ModelForm):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('SE', 'Sin especificar'),
    ]
    
    gender = forms.ChoiceField(choices=GENERO_CHOICES, label='Género', widget=forms.Select(attrs={'class': 'form-select', 'id': 'genero-select'}))
    formatted_phone_number = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'formatted_phone_number'}), required=False)

    class Meta:
        model = User
        fields = [
            'name',
            'last_name',
            'birthday',
            'phone_number',
            'comuna',
            'gender',
            'email',
            'password',
        ]
        labels = {  # Etiquetas para los CAMPOS
            'name': 'Nombre',
            'last_name': 'Apellido',
            'birthday': 'Fecha de nacimiento',
            'phone_number': 'Teléfono',
            'comuna': 'Comuna',
            'gender': 'Género', 
            'email': 'Correo',
            'password': 'Contraseña',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su nombre', 'id': 'idNombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido', 'id': 'idApellido'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'idFecha_nac'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '9 1234 5678', 'type': 'tel', 'id': 'idFono'}),
            'comuna': forms.Select(attrs={'class': 'form-select', 'id': 'comuna-select'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'genero-select'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su correo', 'id': 'idCorreo'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su contraseña', 'id': 'idContraseña', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
