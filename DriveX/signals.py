# Archivo: DriveX/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
import logging

# Configura un logger para registrar eventos o errores importantes
logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def asignar_grupo_cliente(sender, instance, created, **kwargs):
    """
    Asigna automáticamente a un usuario recién creado al grupo 'Clientes'.

    Esta señal se activa después de que se guarda un objeto User.
    Si el usuario es nuevo (created=True), se le intenta asignar al grupo.
    Es crucial que el grupo 'Clientes' exista en la base de datos.
    """
    if created:
        try:
            # Es más eficiente usar .get() directamente si esperas que exista
            grupo_clientes = Group.objects.get(name='Clientes')
            instance.groups.add(grupo_clientes)
        except Group.DoesNotExist:
            # En lugar de imprimir, registra una advertencia.
            # Esto es más flexible y se puede configurar en producción.
            logger.warning(
                "El grupo 'Clientes' no existe. No se pudo asignar al nuevo usuario '%s'. "
                "Crea el grupo en el panel de administración de Django.",
                instance.username
            )