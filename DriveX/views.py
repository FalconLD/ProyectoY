from django.shortcuts import render

def index(request):
    return render(request, 'DriveX/index.html')

def vehiculos(request):
    return render(request, 'DriveX/vehiculos.html')

def reserva(request):
    return render(request, 'DriveX/reserva.html')