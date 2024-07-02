from django.contrib import admin
from .models import SolicitudProducto





class SolicitudProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user_name', 'product', 'quantity')
    # ordering = ('get_user_name',)


    def get_user_name(self, obj):
        return f"{obj.user.name} {obj.user.last_name}"

    get_user_name.short_description = 'Nombre Solicitante'  # Nombre de la columna en el admin

admin.site.register(SolicitudProducto,SolicitudProductoAdmin)