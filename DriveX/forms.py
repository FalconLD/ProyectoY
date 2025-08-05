# Archivo: DriveX/forms.py

from django import forms
from .models import Reserva, Vehiculo

class ReservaForm(forms.ModelForm):
    # Hacemos que el campo de vehículo sea un queryset para que se muestre correctamente
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.all(), empty_label="Selecciona un vehículo")

    class Meta:
        model = Reserva
        fields = [
            'vehiculo', 'nombre_completo', 'email', 'telefono', 
            'fecha_servicio', 'hora_servicio', 'duracion', 
            'tipo_servicio', 'direccion_recogida', 'destino', 
            'solicitudes_especiales'
        ]
        # Usamos widgets para definir el tipo de input en HTML
        widgets = {
            'fecha_servicio': forms.DateInput(attrs={'type': 'date'}),
            'hora_servicio': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Con este bucle, añadimos placeholders y clases a todos los campos
        # para que coincidan con tus estilos CSS sin tener que hacerlo en el HTML.
        
        placeholders = {
            'nombre_completo': 'Tu Nombre Completo',
            'email': 'tu.correo@ejemplo.com',
            'telefono': '+123 456 7890',
            'direccion_recogida': 'Ingresa la dirección de recogida',
            'destino': 'Ingresa el destino (opcional)',
            'solicitudes_especiales': 'Compártenos cualquier preferencia o requerimiento especial...'
        }

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs['placeholder'] = placeholder

        # Opcional: Añadir una clase común a todos los campos para estilos
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-input'