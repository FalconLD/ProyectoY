from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # ... (tus URLs principales sin cambios) ...
    path('', views.index, name='index'),
    path('vehiculos/', views.lista_categorias, name='vehiculos'),
    path('vehiculos/<slug:categoria_slug>/', views.vehiculos_por_categoria, name='vehiculos_por_categoria'),
    path('pilotos/', views.pilotos_view, name='pilotos'),
    path('reserva/', views.reserva, name='reserva'),
    path('contacto/', views.contacto, name='contacto'),
    path('faq/', views.faq, name='faq'),
    path('terminos/', views.terminos, name='terminos'),
    path('sobre-nosotros/', views.sobre_nosotros, name='sobre_nosotros'),
    path('promociones/', views.promociones, name='promociones'),
    path('calcular-ruta/', views.calcular_ruta, name='calcular_ruta'),

    
    # ... (tus URLs de autenticación sin cambios) ...
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='DriveX/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='DriveX/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='DriveX/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='DriveX/password_reset_complete.html'), name='password_reset_complete'),

    # ==== PANEL DE ADMINISTRACIÓN REESTRUCTURADO ====
    path('panel/', views.panel_administracion, name='panel_administracion'), # Esta es ahora la página "hub"
    path('panel/flota/', views.panel_flota, name='panel_flota'), # NUEVA RUTA
    path('panel/mantenimiento/', views.panel_mantenimiento, name='panel_mantenimiento'), # NUEVA RUTA
    
    # --- CRUD de Vehículos (se mantienen igual) ---
    path('panel/vehiculo/nuevo/', views.vehiculo_add, name='vehiculo_add'),
    path('panel/vehiculo/editar/<int:pk>/', views.vehiculo_edit, name='vehiculo_edit'),
    path('panel/vehiculo/eliminar/<int:pk>/', views.vehiculo_delete, name='vehiculo_delete'),
    
    # --- Gestión de Reservas (se mantienen igual) ---
    path('panel/reservas/', views.panel_reservas, name='panel_reservas'),
    path('panel/reservas/update/<int:pk>/', views.update_reserva_status, name='update_reserva_status'),
    path('panel/reservas/exportar-csv/', views.exportar_reservas_csv, name='exportar_reservas_csv'),
]