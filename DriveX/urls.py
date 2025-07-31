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

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/', views.lista_categorias, name='vehiculos'),
    path('vehiculos/<slug:categoria_slug>/', views.vehiculos_por_categoria, name='vehiculos_por_categoria'),
    path('reserva/', views.reserva, name='reserva'),
    path('contacto/', views.contacto, name='contacto'),
    path('faq/', views.faq, name='faq'),
    path('terminos/', views.terminos, name='terminos'),
    path('login/', views.login, name='login'),
    path('registro/', views.registro, name='registro'),
    path('electricos/', views.electricos, name='electricos'),
    path('hibridos/', views.hibridos, name='hibridos'),
    path('gasolina/', views.gasolina, name='gasolina'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)