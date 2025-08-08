# Archivo: DriveX/utils.py
import heapq

def dijkstra(grafo, inicio, fin):
    """
    Implementación del algoritmo de Dijkstra para encontrar la ruta más corta
    en un grafo ponderado no dirigido.

    Args:
        grafo (dict): Diccionario de diccionarios que representa el grafo.
                      Ej: {'A': {'B': 10}, 'B': {'A': 10}}
        inicio (str): El nodo de inicio.
        fin (str): El nodo de destino.

    Returns:
        tuple: Una tupla con (distancia_total, ruta_como_lista).
               Si no hay ruta, devuelve (float('inf'), []).
    """
    # Cola de prioridad para almacenar (distancia, nodo_actual)
    cola_prioridad = [(0, inicio)]
    
    # Diccionario para las distancias más cortas encontradas hasta ahora
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[inicio] = 0
    
    # Diccionario para reconstruir el camino óptimo
    rutas_previas = {nodo: None for nodo in grafo}

    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)

        # Si ya hemos encontrado un camino más corto a este nodo, lo ignoramos
        if distancia_actual > distancias[nodo_actual]:
            continue

        # Si hemos llegado al destino, podemos terminar
        if nodo_actual == fin:
            break

        # Exploramos los vecinos del nodo actual
        for vecino, peso in grafo[nodo_actual].items():
            nueva_distancia = distancia_actual + peso
            
            # Si encontramos un camino más corto hacia el vecino
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                rutas_previas[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))

    # Reconstrucción de la ruta desde el final hasta el inicio
    ruta_optima = []
    paso_actual = fin
    
    # Solo reconstruimos si se encontró una ruta (la distancia no es infinita)
    if distancias[paso_actual] != float('infinity'):
        while paso_actual is not None:
            ruta_optima.insert(0, paso_actual) # Insertamos al inicio para tener el orden correcto
            paso_actual = rutas_previas[paso_actual]
    
    return distancias[fin], ruta_optima