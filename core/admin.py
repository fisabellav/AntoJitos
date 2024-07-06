from django.contrib import admin
from .models import Order
from .models import OrderDetail





class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'quantity')



admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)