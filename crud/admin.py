from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at','updated_at')
    list_display = ('id','product')
    ordering = ('product',)

class FlavorAdmin(admin.ModelAdmin):
    list_display = ('id','flavor')
    ordering = ('id',)

admin.site.register(Flavor, FlavorAdmin)
admin.site.register(Product,ProductAdmin)
