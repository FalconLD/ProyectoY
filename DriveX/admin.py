from django.contrib import admin
from .models import Categoria, Vehiculo, Reserva

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'es_destacado')
    list_filter = ('categoria', 'es_destacado')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('es_destacado',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('vehiculo', 'usuario', 'fecha_servicio', 'fecha_creacion')
    list_filter = ('fecha_servicio', 'vehiculo')
    