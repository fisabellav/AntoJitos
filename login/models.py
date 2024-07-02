from django.db import models
import re
from datetime import datetime, timedelta

# Create your models here.
class UserManager(models.Manager):
    def validador_campos(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        JUST_LETTERS = re.compile(r'^[a-zA-Z.]+$')
        PASSWORD_REGEX = re.compile(r'^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])\S{8,16}$')

        errors = {}

        
        if len(postData['first_name'].strip()) < 2 or len(postData['first_name'].strip()) > 30:
            errors['first_name_len'] = "Nombre debe tener entre 2 y 30 caracteres"

        if len(postData['last_name'].strip()) < 2 or len(postData['last_name'].strip()) > 30:
            errors['last_name_len'] = "Apellido debe tener entre 2 y 30 caracteres"
        
        if not JUST_LETTERS.match(postData['first_name']) or not JUST_LETTERS.match(postData['last_name']):
            errors['just_letters'] = "Solo se permite el ingreso de letras en el nombre y apellido"
            
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Formato correo no válido"
        
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password_format'] = "Formato contraseña no válido"

        #if len(postData['password']) < 8 or len(postData['password']) > 15:
        #    errors['password_len'] = "La cantidad de caracteres debe ser entre 8 y 15" 

        if postData['password'] != postData['password_confirm']:
            errors['password_confirm'] = "Contraseñas no coinciden"

        return errors

class Comuna(models.Model):
    comuna = models.CharField(verbose_name='COMUNA', max_length=100)

    def __str__(self):
        return self.comuna

def default_birthday():
    return datetime.now().date() - timedelta(days=365*18)

class User(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('SE', 'Sin especificar'),
    ]

    name = models.CharField(verbose_name='NOMBRE', max_length=50, blank=True)
    last_name = models.CharField(verbose_name='APELLIDO', max_length=50, blank=True)
    birthday = models.DateField(verbose_name='FECHA DE NACIMIENTO', default=default_birthday)
    phone_number = models.CharField(verbose_name='TELÉFONO', max_length=15, blank=True)
    gender = models.CharField(verbose_name='GÉNERO', max_length=2, choices=GENERO_CHOICES, default='SE')
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE, verbose_name='COMUNA', blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', max_length=100, unique=True, blank=True)
    password = models.CharField(verbose_name='Clave', max_length=250, null=True, blank=True)
    rol = models.CharField(max_length=20, default='USER')
    created_at = models.DateTimeField(verbose_name='Fecha registro', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización', auto_now=True)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        
    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = 'Nombre por defecto'
        if not self.last_name:
            self.last_name = 'Apellido por defecto'
        if not self.phone_number:
            self.phone_number = 'Teléfono por defecto'
        if not self.email:
            self.email = 'Correo por defecto'
        super().save(*args, **kwargs)  