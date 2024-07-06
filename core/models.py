from django.db import models
from crud.models import Product
from login.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('PC', 'Pendiente Confirmación'),
        ('CF', 'Confirmado'),
        ('EP', 'En preparación'),
        ('EN', 'Entregado'),
        ('CN', 'Cancelado'),
    ]

    user = models.ForeignKey(User, verbose_name='Cliente', on_delete=models.CASCADE)
    total = models.PositiveIntegerField(verbose_name='Total')
    status = models.CharField(verbose_name='Estado', max_length=2, choices=STATUS_CHOICES, default='PC')
    created_at = models.DateTimeField(verbose_name='Fecha registro',auto_now_add=True)

    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'

    def __str__(self):
        return f"{self.user} - {self.product}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name='Pedido', on_delete=models.CASCADE)
    product = models.ForeignKey(Product,verbose_name='Producto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Cantidad')
    unit_price = models.PositiveIntegerField(verbose_name='Precio unitario')
    subtotal = models.PositiveIntegerField(verbose_name='Subtotal')

    class Meta:
        verbose_name = 'detalle solicitud'
        verbose_name_plural = 'detalle solicitudes'

    def __str__(self):
        return f"{self.user} - {self.product}"