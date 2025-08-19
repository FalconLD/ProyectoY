import csv
from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from .models import Vehiculo, Categoria, Reserva, Sucursal, Ruta, Piloto
from .forms import ReservaForm, ContactoForm, VehiculoForm, CustomUserCreationForm
from .utils import dijkstra

# ========= Vistas Principales =========

def index(request):
    vehiculos_destacados = Vehiculo.objects.filter(es_destacado=True)
    context = {'vehiculos_destacados': vehiculos_destacados}
    return render(request, 'DriveX/index.html', context)

def lista_categorias(request):
    search_query = request.GET.get('q', None)
    context = {}
    if search_query:
        vehiculos_encontrados = Vehiculo.objects.filter(nombre__icontains=search_query)
        context['vehiculos'] = vehiculos_encontrados
        context['search_query'] = search_query
    else:
        categorias = Categoria.objects.all()
        context['categorias'] = categorias
    return render(request, 'DriveX/vehiculos.html', context)

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

def calcular_ruta(request):
    sucursales = Sucursal.objects.all()
    origen_pk = request.GET.get('origen')
    destino_pk = request.GET.get('destino')
    
    context = {
        'sucursales': sucursales,
        'origen_pk': int(origen_pk) if origen_pk else None,
        'destino_pk': int(destino_pk) if destino_pk else None,
    }

    if origen_pk and destino_pk and origen_pk != destino_pk:
        rutas = Ruta.objects.all()
        grafo = {s.nombre: {} for s in sucursales}
        for ruta in rutas:
            grafo[ruta.origen.nombre][ruta.destino.nombre] = ruta.distancia
            grafo[ruta.destino.nombre][ruta.origen.nombre] = ruta.distancia

        origen = get_object_or_404(Sucursal, pk=origen_pk)
        destino = get_object_or_404(Sucursal, pk=destino_pk)

        distancia, ruta_optima = dijkstra(grafo, origen.nombre, destino.nombre)

        context['distancia'] = distancia if distancia != float('infinity') else -1
        context['ruta_optima'] = ruta_optima
        
    return render(request, 'DriveX/calcular_ruta.html', context)

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

# ========= VISTA PARA "MIS RESERVAS" (NUEVO) =========
@login_required
def mis_reservas(request):
    """
    Muestra al usuario autenticado una lista con todas sus reservas.
    """
    reservas_usuario = Reserva.objects.filter(usuario=request.user).order_by('-fecha_servicio')
    context = {
        'reservas': reservas_usuario
    }
    return render(request, 'DriveX/mis_reservas.html', context)

# ========= Vistas del Panel de Administración =========

def es_administrador(user):
    return user.is_authenticated and user.groups.filter(name='Administradores').exists()

@user_passes_test(es_administrador, login_url='login')
def panel_administracion(request):
    """
    Esta vista actúa como una página principal o "hub" para las diferentes
    secciones del panel de administración.
    """
    return render(request, 'DriveX/panel_administracion.html')

@user_passes_test(es_administrador, login_url='login')
def panel_flota(request):
    """
    Esta vista muestra la tabla con la flota de vehículos para su gestión (CRUD).
    """
    vehiculos = Vehiculo.objects.all().order_by('categoria', 'nombre')
    context = {'vehiculos': vehiculos}
    return render(request, 'DriveX/panel_flota.html', context)

@user_passes_test(es_administrador, login_url='login')
def panel_mantenimiento(request):
    """
    Esta vista muestra la página informativa sobre los costos de mantenimiento.
    """
    return render(request, 'DriveX/panel_mantenimiento.html')

# --- CRUD de Vehículos ---
@user_passes_test(es_administrador, login_url='login')
def vehiculo_add(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehículo añadido con éxito.')
            return redirect('panel_flota') # CORREGIDO: Redirige al panel de flota
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
            return redirect('panel_flota') # CORREGIDO: Redirige al panel de flota
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
        return redirect('panel_flota') # CORREGIDO: Redirige al panel de flota
    return render(request, 'DriveX/vehiculo_confirm_delete.html', {'vehiculo': vehiculo})

# --- GESTIÓN DE RESERVAS ---
@user_passes_test(es_administrador, login_url='login')
def panel_reservas(request):
    active_filter = request.GET.get('estado', None)
    reservas = Reserva.objects.all().select_related('usuario', 'vehiculo').order_by('-fecha_servicio')

    if active_filter and active_filter in dict(Reserva.ESTADO_CHOICES):
        reservas = reservas.filter(estado=active_filter)
    
    context = {
        'reservas': reservas,
        'estados': dict(Reserva.ESTADO_CHOICES),
        'active_filter': active_filter,
    }
    return render(request, 'DriveX/panel_reservas.html', context)

@user_passes_test(es_administrador, login_url='login')
def update_reserva_status(request, pk):
    if request.method == 'POST':
        reserva = get_object_or_404(Reserva, pk=pk)
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
            reserva.estado = nuevo_estado
            reserva.save()
            messages.success(request, f"El estado de la reserva ha sido actualizado a '{reserva.get_estado_display()}'.")
    return redirect('panel_reservas')

@user_passes_test(es_administrador, login_url='login')
def exportar_reservas_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="reporte_reservas_{datetime.now().strftime("%Y-%m-%d")}.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['ID Reserva', 'Cliente', 'Email', 'Vehículo', 'Fecha Servicio', 'Estado'])
    
    reservas = Reserva.objects.select_related('usuario', 'vehiculo').all()

    for reserva in reservas:
        writer.writerow([
            reserva.pk,
            reserva.usuario.username,
            reserva.email,
            reserva.vehiculo.nombre if reserva.vehiculo else 'N/A',
            reserva.fecha_servicio,
            reserva.get_estado_display()
        ])
    
    return response

def pilotos_view(request):
    pilotos = Piloto.objects.all()
    return render(request, 'DriveX/pilotos.html', {'pilotos': pilotos})