from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User # Importa el modelo de usuario

class Categoria(models.Model):
    nombre = models.CharField(max_length=50, unique=True, help_text="Ej: Gasolina, Eléctrico, Híbrido")
    descripcion = models.TextField(help_text="Una breve descripción sobre este tipo de vehículos.")
    slug = models.SlugField(unique=True, blank=True, help_text="Se genera automáticamente a partir del nombre.")

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
    
    # Relación con la categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='vehiculos')
    
    # Para el formulario de reserva
    valor_slug = models.SlugField(unique=True, help_text="Un identificador único para la URL y el formulario. Ej: mercedes-s")
    
    # Campo para la imagen
    imagen = models.ImageField(upload_to='vehiculos/', help_text="Sube una imagen del vehículo.")
    
    # Para decidir si aparece en la página de inicio
    es_destacado = models.BooleanField(default=False, help_text="Marcar si este vehículo debe aparecer en la sección 'Destacados' de la página de inicio.")

    def __str__(self):
        return self.nombre
    
class Reserva(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) # Enlaza la reserva a un usuario
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

    def __str__(self):
        return f"Reserva de {self.vehiculo.nombre} por {self.usuario.username} para el {self.fecha_servicio}"