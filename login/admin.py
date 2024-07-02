from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')
    list_display = ('id', )
    ordering = ('id',)

class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id','comuna')
    ordering = ('id',)

admin.site.register(Comuna,ComunaAdmin)
admin.site.register(User, UserAdmin)

