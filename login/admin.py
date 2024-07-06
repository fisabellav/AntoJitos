from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', 'get_user_name', 'email', 'phone_number', 'comuna')
    ordering = ('id',)
    
    def get_user_name(self, obj):
        return f"{obj.name} {obj.last_name}"
    get_user_name.short_description = 'Nombre'

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id','comuna')
    ordering = ('id',)

admin.site.register(Comuna,ComunaAdmin)
admin.site.register(User, UserAdmin)

