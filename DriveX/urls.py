# from django.urls import path
# from . import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('', views.index, name='index'),
    
#     # Esta URL ahora mostrará la lista de categorías (Gasolina, Eléctrico, etc.)
#     path('vehiculos/', views.lista_categorias, name='vehiculos'),
    
#     # Nueva URL para ver los vehículos de una categoría específica
#     # Ej: /vehiculos/electrico/
#     path('vehiculos/<slug:categoria_slug>/', views.vehiculos_por_categoria, name='vehiculos_por_categoria'),
    
#     path('reserva/', views.reserva, name='reserva'),
# ]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views # Para 'Olvidaste tu contraseña'

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/', views.lista_categorias, name='vehiculos'),
    path('vehiculos/<slug:categoria_slug>/', views.vehiculos_por_categoria, name='vehiculos_por_categoria'),
    path('reserva/', views.reserva, name='reserva'),
    path('contacto/', views.contacto, name='contacto'),
    path('faq/', views.faq, name='faq'),
    path('terminos/', views.terminos, name='terminos'),
    # path('electricos/', views.electricos, name='electricos'),
    # path('hibridos/', views.hibridos, name='hibridos'),
    # path('gasolina/', views.gasolina, name='gasolina'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'), # Apunta a la nueva vista
    path('logout/', views.logout_view, name='logout'), # Nueva URL para cerrar sesión
     # URLs para restablecer contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='DriveX/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='DriveX/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='DriveX/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='DriveX/password_reset_complete.html'), name='password_reset_complete'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    