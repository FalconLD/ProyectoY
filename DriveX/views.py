from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Vehiculo, Categoria, Reserva
from .forms import ReservaForm, ContactoForm, VehiculoForm, CustomUserCreationForm

# ========= Vistas Principales =========

def index(request):
    vehiculos_destacados = Vehiculo.objects.filter(es_destacado=True)
    context = {'vehiculos_destacados': vehiculos_destacados}
    return render(request, 'DriveX/index.html', context)

def lista_categorias(request):
    """
    Esta vista tiene doble funcionalidad:
    - Si no hay parámetro de búsqueda, muestra la lista de categorías.
    - Si hay un parámetro 'q' en la URL, busca vehículos y muestra los resultados.
    """
    search_query = request.GET.get('q', None)
    
    # --- Línea de depuración ---
    print(f"La consulta de búsqueda recibida es: '{search_query}'")
    
    context = {}
    
    if search_query:
        # Si hay una consulta de búsqueda, filtramos los vehículos.
        vehiculos_encontrados = Vehiculo.objects.filter(nombre__icontains=search_query)
        context['vehiculos'] = vehiculos_encontrados
        context['search_query'] = search_query
    else:
        # Si no hay búsqueda, mostramos las categorías.
        categorias = Categoria.objects.all()
        context['categorias'] = categorias

    return render(request, 'DriveX/vehiculos.html', context)

# SE HA ELIMINADO LA SEGUNDA DEFINICIÓN REDUNDANTE DE 'lista_categorias' QUE ESTABA AQUÍ.

def vehiculos_por_categoria(request, categoria_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    vehiculos = Vehiculo.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'vehiculos': vehiculos}
    return render(request, 'DriveX/vehiculo_catalogo.html', context)

@login_required
def reserva(request):
    initial_data = {}
    vehiculo_slug = request.GET.get('vehicle')
    if vehiculo_slug:
        vehiculo = get_object_or_404(Vehiculo, valor_slug=vehiculo_slug)
        initial_data['vehiculo'] = vehiculo

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.save()
            messages.success(request, '¡Reserva realizada con éxito! Nos contactaremos contigo pronto.')
            return redirect('index')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = ReservaForm(initial=initial_data)

    context = {'form': form}
    return render(request, 'DriveX/reserva.html', context)

def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            messages.success(request, '¡Mensaje enviado con éxito! Te responderemos pronto.')
            return redirect('contacto')
        else:
            messages.error(request, 'Por favor, completa todos los campos obligatorios correctamente.')
    else:
        form = ContactoForm()
    
    return render(request, 'DriveX/contacto.html', {'form': form})

# ========= Vistas de Contenido Estático =========

def faq(request):
    return render(request, 'DriveX/faq.html')

def terminos(request):
    return render(request, 'DriveX/terminos.html')

def sobre_nosotros(request):
    return render(request, 'DriveX/sobre_nosotros.html')

def promociones(request):
    return render(request, 'DriveX/promociones.html')

# ========= Vistas de Autenticación =========

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, '¡Registro exitoso! Has iniciado sesión.')
            return redirect('index')
        else:
            messages.error(request, 'Hubo un error en el registro. Por favor, revisa los datos.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'DriveX/registro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.info(request, f"Has iniciado sesión como {user.username}.")
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'DriveX/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

# ========= Vistas del Panel de Administración =========

def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name='Administradores').exists()

@user_passes_test(es_administrador, login_url='login')
def panel_administracion(request):
    vehiculos = Vehiculo.objects.all().order_by('categoria', 'nombre')
    context = {'vehiculos': vehiculos}
    return render(request, 'DriveX/panel_administracion.html', context)

@user_passes_test(es_administrador, login_url='login')
def vehiculo_add(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo añadido con éxito.')
            return redirect('panel_administracion')
    else:
        form = VehiculoForm()
    
    context = {'form': form, 'form_title': 'Añadir Nuevo Vehículo'}
    return render(request, 'DriveX/vehiculo_form.html', context)

@user_passes_test(es_administrador, login_url='login')
def vehiculo_edit(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES, instance=vehiculo)
        if form.is_valid():
            form.save()
            messages.success(request, f'El vehículo "{vehiculo.nombre}" ha sido actualizado con éxito.')
            return redirect('panel_administracion')
    else:
        form = VehiculoForm(instance=vehiculo)

    context = {'form': form, 'form_title': f'Editar Vehículo: {vehiculo.nombre}'}
    return render(request, 'DriveX/vehiculo_form.html', context)

@user_passes_test(es_administrador, login_url='login')
def vehiculo_delete(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo_nombre = vehiculo.nombre
        vehiculo.delete()
        messages.success(request, f'El vehículo "{vehiculo_nombre}" ha sido eliminado con éxito.')
        return redirect('panel_administracion')
    return render(request, 'DriveX/vehiculo_confirm_delete.html', {'vehiculo': vehiculo})