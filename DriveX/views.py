from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required # Importa el decorador
from .models import Vehiculo, Categoria, Reserva # Añade Reserva
from .forms import ReservaForm # Importa el formulario desde forms.py

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

# VISTA DE RESERVA REAL Y EN SU LUGAR CORRECTO
@login_required # Solo usuarios logueados pueden reservar
def reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user # Asigna el usuario actual
            reserva.save()
            messages.success(request, '¡Reserva realizada con éxito! Nos contactaremos contigo pronto.')
            return redirect('index')
        else:
             messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ReservaForm()
    
    context = {
        'form': form
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

# VISTA DE REGISTRO REAL
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user) # Inicia sesión automáticamente tras el registro
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('index')
        else:
            messages.error(request, 'Hubo un error en el registro. Por favor, revisa los datos.')
    else:
        form = UserCreationForm()
    return render(request, 'DriveX/registro.html', {'form': form})

# VISTA DE LOGIN REAL
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.info(request, f"Has iniciado sesión como {username}.")
                return redirect('index')
            else:
                messages.error(request, "Nombre de usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    form = AuthenticationForm()
    return render(request, 'DriveX/login.html', {'form': form})

# VISTA DE LOGOUT
def logout_view(request):
    auth_logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

@login_required
def panel_administracion(request):
    # PRIMER FILTRO: ¿Ha iniciado sesión el usuario?
    # SEGUNDO FILTRO: ¿Pertenece al grupo 'Administradores'?
    if not request.user.groups.filter(name='Administradores').exists():
        messages.error(request, "No tienes permiso para acceder a esta página.")
        return redirect('index')

    # Si pasa los filtros, le mostramos la página del panel.
    # Por ahora, solo le pasamos una lista de todos los vehículos para que los vea.
    vehiculos = Vehiculo.objects.all()
    context = {
        'vehiculos': vehiculos
    }
    return render(request, 'DriveX/panel_administracion.html', context)