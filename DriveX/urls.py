from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculos/', views.vehiculos, name='vehiculos'),
    path('reserva/', views.reserva, name='reserva'),
]