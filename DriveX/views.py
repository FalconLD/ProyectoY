from django.shortcuts import render
from .models import Vehiculo, Categoria

def index(request):
    # Obtenemos solo los vehículos marcados como 'destacados'
    vehiculos_destacados = Vehiculo.objects.filter(es_destacado=True)
    context = {
        'vehiculos_destacados': vehiculos_destacados
    }
    return render(request, 'DriveX/index.html', context)

def lista_categorias(request):
    # Obtenemos todas las categorías para listarlas
    categorias = Categoria.objects.all()
    context = {
        'categorias': categorias
    }
    return render(request, 'DriveX/vehiculos.html', context)

def vehiculos_por_categoria(request, categoria_slug):
    # Obtenemos la categoría específica por su slug
    categoria = Categoria.objects.get(slug=categoria_slug)
    # Obtenemos todos los vehículos que pertenecen a esa categoría
    vehiculos = Vehiculo.objects.filter(categoria=categoria)
    context = {
        'categoria': categoria,
        'vehiculos': vehiculos
    }
    # Reutilizaremos una nueva plantilla para mostrar esta lista
    return render(request, 'DriveX/vehiculos_catalogo.html', context)

def reserva(request):
    # Pasamos todos los vehículos al formulario para el selector
    todos_los_vehiculos = Vehiculo.objects.all()
    # Aquí iría tu lógica para manejar el método POST del formulario
    if request.method == 'POST':
        # ... procesar formulario ...
        pass
    
    context = {
        'vehiculos': todos_los_vehiculos
    }
    return render(request, 'DriveX/reserva.html', context)