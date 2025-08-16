from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Gasolina, Eléctrico, Híbrido")
    descripcion = models.TextField(help_text="Una breve descripción sobre este tipo de vehículos.")
    slug = models.SlugField(unique=True, blank=True, help_text="Se genera automáticamente a partir del nombre.")

    class Meta:
        verbose_name_plural = "Categorías"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    nombre = models.CharField(max_length=100, help_text="Ej: Mercedes-Benz Clase S")
    descripcion = models.TextField(help_text="Descripción principal del vehículo.")
    caracteristicas = models.CharField(max_length=255, help_text="Características breves separadas por comas. Ej: Asientos de cuero, climatización, etc.")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='vehiculos')
    valor_slug = models.SlugField(unique=True, help_text="Un identificador único para la URL y el formulario. Ej: mercedes-s")
    imagen = models.ImageField(upload_to='vehiculos/', help_text="Sube una imagen del vehículo.")
    es_destacado = models.BooleanField(default=False, help_text="Marcar si este vehículo debe aparecer en la sección 'Destacados' de la página de inicio.")

    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    ESTADO_PENDIENTE = 'PENDIENTE'
    ESTADO_CONFIRMADA = 'CONFIRMADA'
    ESTADO_FINALIZADA = 'FINALIZADA'
    ESTADO_CANCELADA = 'CANCELADA'

    ESTADO_CHOICES = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_FINALIZADA, 'Finalizada'),
        (ESTADO_CANCELADA, 'Cancelada'),
    ]

    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, related_name='reservas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_servicio = models.DateField()
    hora_servicio = models.TimeField()
    duracion = models.CharField(max_length=50)
    tipo_servicio = models.CharField(max_length=50)
    direccion_recogida = models.CharField(max_length=255)
    destino = models.CharField(max_length=255, blank=True, null=True)
    solicitudes_especiales = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PENDIENTE,
        help_text="El estado actual de la reserva"
    )

    def __str__(self):
        vehiculo_nombre = self.vehiculo.nombre if self.vehiculo else "Vehículo no disponible"
        return f"Reserva de {vehiculo_nombre} por {self.usuario.username} para el {self.fecha_servicio}"

class Sucursal(models.Model):
    """ Representa un nodo en el grafo de sucursales. """
    nombre = models.CharField(max_length=100, unique=True, help_text="Nombre de la sucursal (ej. Quito Norte)")
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class Ruta(models.Model):
    """ Representa una arista ponderada entre dos sucursales (nodos). """
    origen = models.ForeignKey(Sucursal, related_name='rutas_salida', on_delete=models.CASCADE)
    destino = models.ForeignKey(Sucursal, related_name='rutas_llegada', on_delete=models.CASCADE)
    distancia = models.PositiveIntegerField(help_text="Distancia en kilómetros entre las dos sucursales.")

    class Meta:
        unique_together = ('origen', 'destino')

    def __str__(self):
        return f"Ruta de {self.origen.nombre} a {self.destino.nombre} ({self.distancia} km)"