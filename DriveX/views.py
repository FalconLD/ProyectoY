from django.shortcuts import render, redirect
from django.contrib import messages
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
    return render(request, 'DriveX/vehiculo_catalogo.html', context)

def reserva(request):
    todos_los_vehiculos = Vehiculo.objects.all()
    if request.method == 'POST':
        # Lógica básica para manejar el formulario (puedes expandirla)
        nombre = request.POST.get('name')
        email = request.POST.get('email')
        telefono = request.POST.get('phone')
        vehiculo_id = request.POST.get('vehicle')
        fecha = request.POST.get('date')
        hora = request.POST.get('time')
        duracion = request.POST.get('duration')
        tipo_servicio = request.POST.get('tipo_servicio')
        direccion_recogida = request.POST.get('pickup-address')
        
        if all([nombre, email, telefono, vehiculo_id, fecha, hora, duracion, tipo_servicio, direccion_recogida]):
            messages.success(request, '¡Reserva realizada con éxito! Nos contactaremos contigo pronto.')
            return redirect('reserva')
        else:
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
    
    context = {
        'vehiculos': todos_los_vehiculos
    }
    return render(request, 'DriveX/reserva.html', context)

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        if all([nombre, email, asunto, mensaje]):
            messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
    
    return render(request, 'DriveX/contacto.html')

def faq(request):
    # No requiere lógica dinámica por ahora, solo muestra la plantilla
    return render(request, 'DriveX/faq.html')

def terminos(request):
    # No requiere lógica dinámica por ahora, solo muestra la plantilla
    return render(request, 'DriveX/terminos.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Aquí deberías agregar autenticación (por ejemplo, con Django auth)
        if username and password:  # Simulación básica
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('index')
        else:
            messages.error(request, 'Credenciales incorrectas o campos vacíos.')
    
    return render(request, 'DriveX/login.html')

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        licencia = request.POST.get('licencia')
        
        if all([nombre, email, password, licencia]):
            # Aquí deberías guardar el usuario en la base de datos (usar Django auth)
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Por favor, completa todos los campos obligatorios.')
    
    return render(request, 'DriveX/registro.html')

def electricos(request):
    categoria = Categoria.objects.get(slug='electricos')
    vehiculos = Vehiculo.objects.filter(categoria=categoria)
    context = {
        'categoria': categoria,
        'vehiculos': vehiculos
    }
    return render(request, 'DriveX/electricos.html', context)

def hibridos(request):
    categoria = Categoria.objects.get(slug='hibridos')
    vehiculos = Vehiculo.objects.filter(categoria=categoria)
    context = {
        'categoria': categoria,
        'vehiculos': vehiculos
    }
    return render(request, 'DriveX/hibridos.html', context)

def gasolina(request):
    categoria = Categoria.objects.get(slug='gasolina')
    vehiculos = Vehiculo.objects.filter(categoria=categoria)
    context = {
        'categoria': categoria,
        'vehiculos': vehiculos
    }
    return render(request, 'DriveX/gasolina.html', context)