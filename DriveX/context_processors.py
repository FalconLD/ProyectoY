# Archivo: DriveX/context_processors.py

def admin_group_processor(request):
    """
    Añade una variable de contexto 'is_in_admin_group' si el usuario
    autenticado pertenece al grupo 'Administradores'.
    """
    is_admin = False
    # Primero, asegúrate de que el usuario está autenticado
    if request.user.is_authenticated:
        # .exists() es una forma eficiente de comprobar si existe al menos un resultado
        is_admin = request.user.groups.filter(name='Administradores').exists()
    
    # Devuelve un diccionario. La clave estará disponible en todas las plantillas.
    return {
        'is_in_admin_group': is_admin
    }