from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Reserva, Vehiculo, Categoria

# Heredamos de UserCreationForm para poder personalizarlo si es necesario en el futuro
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Podrías añadir más campos aquí si modificas el modelo de usuario
        fields = UserCreationForm.Meta.fields


class ReservaForm(forms.ModelForm):
    vehiculo = forms.ModelChoiceField(
        queryset=Vehiculo.objects.all().order_by('nombre'), 
        empty_label="Selecciona un vehículo",
        label="Vehículo"
    )

    class Meta:
        model = Reserva
        fields = [
            'vehiculo', 'nombre_completo', 'email', 'telefono', 
            'fecha_servicio', 'hora_servicio', 'duracion', 
            'tipo_servicio', 'direccion_recogida', 'destino', 
            'solicitudes_especiales'
        ]
        
        # =================================================================
        # LÍNEA CLAVE AÑADIDA:
        # Excluimos los campos que se asignan automáticamente en la vista.
        # Esto soluciona el error que impedía que el formulario se guardara.
        exclude = ['usuario', 'estado']
        # =================================================================

        widgets = {
            'fecha_servicio': forms.DateInput(attrs={'type': 'date'}),
            'hora_servicio': forms.TimeInput(attrs={'type': 'time'}),
            'solicitudes_especiales': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'nombre_completo': 'Nombre Completo',
            'email': 'Correo Electrónico',
            'telefono': 'Teléfono de Contacto',
            'fecha_servicio': 'Fecha del Servicio',
            'hora_servicio': 'Hora del Servicio',
            'duracion': 'Duración del Alquiler (Ej: 24 horas)',
            'tipo_servicio': 'Tipo de Servicio (Ej: Con chofer)',
            'direccion_recogida': 'Dirección de Recogida',
            'destino': 'Destino (Opcional)',
            'solicitudes_especiales': 'Solicitudes Especiales',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'nombre_completo': 'Tu Nombre Completo',
            'email': 'tu.correo@ejemplo.com',
            'telefono': '+123 456 7890',
            'duracion': 'Ej: 1 día, 8 horas, etc.',
            'tipo_servicio': 'Ej: Traslado al aeropuerto, evento especial...',
            'direccion_recogida': 'Ingresa la dirección de recogida',
            'destino': 'Ingresa el destino (opcional)',
            'solicitudes_especiales': 'Compártenos cualquier preferencia...'
        }

        # Añadimos placeholders y una clase CSS común a los campos
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]


class VehiculoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label="Categoría",
        empty_label="Selecciona una categoría"
    )

    class Meta:
        model = Vehiculo
        fields = ['nombre', 'categoria', 'descripcion', 'caracteristicas', 'valor_slug', 'imagen', 'es_destacado']
        labels = {
            'nombre': 'Nombre del Vehículo',
            'descripcion': 'Descripción Completa',
            'caracteristicas': 'Características Principales',
            'valor_slug': 'Identificador URL (slug)',
            'imagen': 'Imagen del Vehículo',
            'es_destacado': '¿Es un vehículo destacado?',
        }
        help_texts = {
            'valor_slug': 'Un identificador único para la URL, sin espacios ni caracteres especiales. Ej: "mercedes-clase-s".',
            'es_destacado': 'Márcalo para que aparezca en la página de inicio.',
            'caracteristicas': 'Separadas por coma. Ej: Asientos de cuero, Techo panorámico.'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'


class ContactoForm(forms.Form):
    nombre = forms.CharField(
        max_length=100, 
        label="Nombre Completo",
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre completo'})
    )
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'tu.correo@ejemplo.com'})
    )
    asunto = forms.CharField(
        max_length=150, 
        label="Asunto",
        widget=forms.TextInput(attrs={'placeholder': 'Motivo de tu consulta'})
    )
    mensaje = forms.CharField(
        label="Mensaje",
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Escribe tu mensaje aquí...'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade una clase común a todos los campos para estilos
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-input'