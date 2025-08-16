from django.contrib import admin
from .models import Categoria, Vehiculo, Reserva, Piloto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}
    search_fields = ('nombre',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'es_destacado')
    list_filter = ('categoria', 'es_destacado')
    search_fields = ('nombre', 'descripcion', 'categoria__nombre')
    list_editable = ('es_destacado',)
    prepopulated_fields = {'valor_slug': ('nombre',)}

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('get_vehiculo_nombre', 'usuario', 'fecha_servicio', 'fecha_creacion')
    list_filter = ('fecha_servicio', 'vehiculo__nombre')
    search_fields = ('usuario__username', 'vehiculo__nombre', 'email')
    list_select_related = ('vehiculo', 'usuario') # Optimiza la consulta a la BD

    def get_vehiculo_nombre(self, obj):
        return obj.vehiculo.nombre if obj.vehiculo else "N/A"
    get_vehiculo_nombre.short_description = 'Vehículo'

admin.site.register(Piloto) # Registro simple sin personalización