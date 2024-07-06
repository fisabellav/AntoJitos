from django.db import models

# Create your models here.
class Flavor(models.Model):
    flavor = models.CharField(verbose_name='SABOR', max_length=100)

    class Meta:
        verbose_name = 'sabor'
        verbose_name_plural = 'sabores'

    def __str__(self):
        return self.flavor

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('GA', 'Galletas'),
        ('PA', 'Pasteles'),
        ('DE', 'Desayuno'),
    ]


    product = models.CharField(verbose_name='Producto', max_length=50)
    description = models.TextField(verbose_name='Descripción',null=True,blank=True)
    category = models.CharField(verbose_name='Categoría', max_length=2, choices=CATEGORY_CHOICES, default='GA')
    price = models.PositiveIntegerField(verbose_name='Precio')
    flavor = models.ManyToManyField(Flavor, verbose_name='Sabor', blank=True)
    image = models.ImageField(verbose_name='Imagen',upload_to='productos',null=True,blank=True)
    created_at = models.DateTimeField(verbose_name='Fecha registro',auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Fecha actualización',auto_now=True)

    class Meta:
        verbose_name = 'producto'
        verbose_name_plural = 'productos'
        ordering = ['product']

    def __str__(self) -> str:
        return self.product